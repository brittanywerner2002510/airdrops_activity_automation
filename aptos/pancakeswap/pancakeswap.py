import logging
import time
from decimal import Decimal

from aptos_sdk.account import Account
from aptos_sdk.bcs import Serializer
from aptos_sdk.client import ResourceNotFound
from aptos_sdk.transactions import TransactionArgument, EntryFunction, TransactionPayload
from aptos_sdk.type_tag import TypeTag, StructTag

from aptos.RestClientWithProxy import RestClientWithProxy
from aptos.token_addresses import TOKENS


class PancakeSwap:
    __router_address = "0xc7efb4076dbe143cbcd98cfaaa929ecfc8f299203dfff63b95ccb6bfe19850fa"
    aptos_address = "0x1::aptos_coin::AptosCoin"

    def __init__(self, private_key: str, node: str = "https://rpc.ankr.com/http/aptos/v1", proxy: str = None,
                 slippage_tolerance: int = 1, user_agent=None, logger: logging.Logger = None):
        self.logger = logger or logging
        self.account = Account.load_key(private_key)
        self.slippage = slippage_tolerance
        self.rest_client = RestClientWithProxy(node, proxy={'http': proxy, 'https': proxy},
                                               user_agent=user_agent, logger=self.logger)
        self.rest_client.client_config.max_gas_amount = 1000

    def register_coin(self, token: str) -> str:
        payload = EntryFunction.natural(
            f"0x1::managed_coin",
            "register",
            [
                TypeTag(StructTag.from_str(token)),
            ],
            [
            ]
        )
        signed_tx = self.rest_client.create_bcs_signed_transaction(self.account, TransactionPayload(payload))
        tx = self.rest_client.submit_bcs_transaction(signed_tx)
        time.sleep(30)
        self.rest_client.wait_for_transaction(tx)
        return tx

    def __estimate_output(self, payload: str, to_token: str) -> int:
        to_token_balance_before_simulate = int(
            self.rest_client.account_resource(self.account.address(), f"0x1::coin::CoinStore<{to_token}>")[
                "data"]["coin"]["value"])
        max_gas_limit = 100
        logging.warning(f"I will use max gas limit {max_gas_limit} while estimation")
        predefined_value = self.rest_client.client_config.max_gas_amount
        self.rest_client.client_config.max_gas_amount = max_gas_limit
        signed_tx = self.rest_client.create_bcs_transaction(
            self.account, TransactionPayload(payload))
        self.rest_client.client_config.max_gas_amount = predefined_value
        tx_info = self.rest_client.simulate_transaction(signed_tx, self.account)[0]
        if tx_info["success"]:
            for change in tx_info["changes"]:
                if change["data"]["type"] == f"0x1::coin::CoinStore<{to_token}>":
                    if change["data"]["type"] == f"0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>":
                        estimated_amount_after_tx = int(change["data"]["data"]["coin"]["value"])
                        return int(Decimal(str((estimated_amount_after_tx - to_token_balance_before_simulate) / 100)) *
                                   (100 - self.slippage))
                    estimated_amount_after_tx = int(change["data"]["data"]["coin"]["value"])
                    return int(Decimal(str(((estimated_amount_after_tx - to_token_balance_before_simulate) / 100))) *
                               (100 - self.slippage))

        return -1

    def swap(self, amount: Decimal, from_token: str, to_token: str) -> str:
        decimals_from = Decimal(self.rest_client.account_resource(
            from_token.split("::")[0], f"0x1::coin::CoinInfo<{from_token}>")["data"]["decimals"])
        try:
            self.rest_client.account_resource(self.account.address(), f"0x1::coin::CoinStore<{to_token}>")
        except ResourceNotFound:
            logging.warning("I never received this coin. Adding to my wallet")
            self.register_coin(to_token)
        if from_token == self.aptos_address or to_token == self.aptos_address:
            payload = EntryFunction.natural(
                f"{self.__router_address}::router",
                "swap_exact_input",
                [
                    TypeTag(StructTag.from_str(from_token)), TypeTag(StructTag.from_str(to_token))
                ],
                [
                    TransactionArgument(int(amount * (10 ** decimals_from)), Serializer.u64),
                    TransactionArgument(0, Serializer.u64),
                ]
            )
            min_amount = self.__estimate_output(payload, to_token)
            if min_amount < 0:
                raise ValueError("Cannot estimate minimal amount for swap on PancakeSwap")
            payload = EntryFunction.natural(
                f"{self.__router_address}::router",
                "swap_exact_input",
                [
                    TypeTag(StructTag.from_str(from_token)), TypeTag(StructTag.from_str(to_token))
                ],
                [
                    TransactionArgument(int(amount * (10 ** decimals_from)), Serializer.u64),
                    TransactionArgument(min_amount, Serializer.u64),
                ]
            )
        else:
            payload = EntryFunction.natural(
                f"{self.__router_address}::router",
                "swap_exact_input_doublehop",
                [
                    TypeTag(StructTag.from_str(from_token)),
                    TypeTag(StructTag.from_str(self.aptos_address)),
                    TypeTag(StructTag.from_str(to_token))
                ],
                [
                    TransactionArgument(int(amount * (10 ** decimals_from)), Serializer.u64),
                    TransactionArgument(0, Serializer.u64),
                ]
            )
            min_amount = self.__estimate_output(payload, to_token)
            if min_amount < 0:
                raise ValueError("Cannot estimate minimal amount for swap on PancakeSwap")
            payload = EntryFunction.natural(
                f"{self.__router_address}::router",
                "swap_exact_input_doublehop",
                [
                    TypeTag(StructTag.from_str(from_token)),
                    TypeTag(StructTag.from_str(self.aptos_address)),
                    TypeTag(StructTag.from_str(to_token))
                ],
                [
                    TransactionArgument(int(amount * (10 ** decimals_from)), Serializer.u64),
                    TransactionArgument(min_amount, Serializer.u64),
                ]
            )
        signed_tx = self.rest_client.create_bcs_signed_transaction(self.account, TransactionPayload(payload))
        return self.rest_client.submit_bcs_transaction(signed_tx)

    def add_liquidity_for_apt(self, token: str, amount: Decimal) -> str:
        decimals_token = Decimal(self.rest_client.account_resource(
            token.split("::")[0], f"0x1::coin::CoinInfo<{token}>")["data"]["decimals"])
        decimals_apt = Decimal(self.rest_client.account_resource(
            self.aptos_address.split("::")[0], f"0x1::coin::CoinInfo<{self.aptos_address}>")["data"]["decimals"])

        reserves = self.rest_client.account_resource(
            self.__router_address, f"{self.__router_address}::swap::TokenPairReserve<{self.aptos_address}, {token}>")

        exchange_rate = (Decimal(reserves["data"]["reserve_x"]) / (10 ** decimals_apt)) / (
                Decimal(reserves["data"]["reserve_y"]) / (10 ** decimals_token))
        calc_apt_amount = Decimal(amount * exchange_rate) * (10 ** decimals_apt)
        calc_apt_amount_minus_slippage = int((calc_apt_amount / 100) * 98)
        token_amount_minus_slippage = int(((amount * (10 ** decimals_token)) / 100) * 98)

        payload = EntryFunction.natural(
            f"{self.__router_address}::router",
            "add_liquidity",
            [
                TypeTag(StructTag.from_str(self.aptos_address)),
                TypeTag(StructTag.from_str(token))
            ],
            [
                TransactionArgument(int(calc_apt_amount), Serializer.u64),
                TransactionArgument(int(amount * (10 ** decimals_token)), Serializer.u64),
                TransactionArgument(calc_apt_amount_minus_slippage, Serializer.u64),
                TransactionArgument(token_amount_minus_slippage, Serializer.u64),
            ]
        )
        signed_tx = self.rest_client.create_bcs_signed_transaction(self.account, TransactionPayload(payload))
        return self.rest_client.submit_bcs_transaction(signed_tx)

    def remove_liquidity_for_apt(self, token: str, amount_liquidity: Decimal | int) -> str:

        supply_amount = int(self.rest_client.account_resource(
            self.__router_address,
            f"0x1::coin::CoinInfo<{self.__router_address}::swap::LPToken"
            f"<{self.aptos_address},{token}>>")['data']['supply']['vec'][0]['integer']['vec'][0]['value'])
        pool_percent = Decimal(amount_liquidity) / Decimal(supply_amount)
        reserves = self.rest_client.account_resource(
            self.__router_address, f"{self.__router_address}::swap::TokenPairReserve<{self.aptos_address}, {token}>")
        token_x = Decimal(reserves["data"]["reserve_x"]) * pool_percent
        token_y = Decimal(reserves["data"]["reserve_y"]) * pool_percent
        token_x_minus_slippage = int(token_x / 100 * 99)
        token_y_minus_slippage = int(token_y / 100 * 99)

        payload = EntryFunction.natural(
            f"{self.__router_address}::router",
            "remove_liquidity",
            [
                TypeTag(StructTag.from_str(self.aptos_address)),
                TypeTag(StructTag.from_str(token))
            ],
            [
                TransactionArgument(int(amount_liquidity), Serializer.u64),
                TransactionArgument(token_x_minus_slippage, Serializer.u64),
                TransactionArgument(token_y_minus_slippage, Serializer.u64),
            ]
        )
        signed_tx = self.rest_client.create_bcs_signed_transaction(self.account, TransactionPayload(payload))
        return self.rest_client.submit_bcs_transaction(signed_tx)

    def exchange_with_amount_in_percent(self, percent: Decimal, route: str, save_apt_amount: Decimal | int = 0) -> str:
        token_from, token_to = TOKENS[route[0]], TOKENS[route[1]]
        decimals_from = Decimal(self.rest_client.account_resource(
            token_from.split("::")[0], f"0x1::coin::CoinInfo<{token_from}>")["data"]["decimals"])

        if route[0] == "APT":
            token_balance = save_apt_amount if save_apt_amount > 0 else (
                Decimal(self.rest_client.account_resource(
                    self.account.address(), f"0x1::coin::CoinStore<{token_from}>")["data"]["coin"]["value"]))
        else:
            token_balance = Decimal(self.rest_client.account_resource(
                self.account.address(), f"0x1::coin::CoinStore<{token_from}>")["data"]["coin"]["value"])
        swap_amount = Decimal(int((token_balance / 100) * percent))
        return self.swap(swap_amount / (10 ** decimals_from), token_from, token_to)

    def add_in_pool_for_apt_with_amount_in_percent(self, token: str, percent: Decimal) -> str | None:
        decimals_from = Decimal(self.rest_client.account_resource(
            TOKENS[token].split("::")[0], f"0x1::coin::CoinInfo<{TOKENS[token]}>")["data"]["decimals"])
        try:
            token_balance = Decimal(self.rest_client.account_resource(
                self.account.address(), f"0x1::coin::CoinStore<{TOKENS[token]}>")["data"]["coin"]["value"])
        except ResourceNotFound:
            self.logger.warning(f"We cannot invest to pool {token}/APT on pancakeswap")
            return None

        if token_balance == 0:
            self.logger.warning(f"We dont invest to pool {token}/APT on pancakeswap")
            return None

        swap_amount = Decimal(int((token_balance / 100) * percent))
        return self.add_liquidity_for_apt(TOKENS[token], swap_amount / (10 ** decimals_from))

    def remove_from_pool_for_apt_with_amount_in_percent(self, token: str, percent: Decimal) -> str | None:
        try:
            token_balance = Decimal(self.rest_client.account_resource(
                self.account.address(),
                f"0x1::coin::CoinStore<{self.__router_address}::swap::LPToken"
                f"<{self.aptos_address}, {TOKENS[token]}>>")["data"]["coin"]["value"])
        except ResourceNotFound:
            self.logger.warning(f"We dont invest to pool {token}/APT on pancakeswap")
            return None

        if token_balance == 0:
            self.logger.warning(f"We dont invest to pool {token}/APT on pancakeswap")
            return None

        remove_liquidity_amount = int(token_balance / 100 * percent)
        return self.remove_liquidity_for_apt(TOKENS[token], remove_liquidity_amount)

    def get_transaction_status(self, tx: str) -> bool:
        if tx is None:
            return True
        try:
            self.rest_client.wait_for_transaction(tx)
            return True
        except AssertionError:
            return False

    def is_swap_to_apt_covers_fee(self, token):
        amount = Decimal(self.rest_client.account_resource(
            self.account.address(), f"0x1::coin::CoinStore<{token}>")["data"]["coin"]["value"])
        apt_amount_before_tx = Decimal(self.rest_client.account_resource(
            self.account.address(), f"0x1::coin::CoinStore<{self.aptos_address}>")["data"]["coin"]["value"])

        payload = EntryFunction.natural(
            f"{self.__router_address}::router",
            "swap_exact_input",
            [
                TypeTag(StructTag.from_str(token)), TypeTag(StructTag.from_str(self.aptos_address))
            ],
            [
                TransactionArgument(int(amount), Serializer.u64),
                TransactionArgument(0, Serializer.u64),
            ]
        )
        max_gas_limit = 100
        logging.warning(f"I will use max gas limit {max_gas_limit} while estimation")
        predefined_value = self.rest_client.client_config.max_gas_amount
        self.rest_client.client_config.max_gas_amount = max_gas_limit
        signed_transaction = self.rest_client.create_bcs_transaction(
            self.account, TransactionPayload(payload)
        )
        self.rest_client.client_config.max_gas_amount = predefined_value
        tx_info = self.rest_client.simulate_transaction(signed_transaction, self.account)[0]
        if tx_info["success"]:
            for change in tx_info["changes"]:
                if change["data"]["type"] == "0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>":
                    estimated_amount_after_tx = int(change["data"]["data"]["coin"]["value"])
                    if estimated_amount_after_tx >= apt_amount_before_tx:
                        return True
                    else:
                        return False
            return False
