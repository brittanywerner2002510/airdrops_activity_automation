import logging
import time
from decimal import Decimal

from aptos_sdk.account import Account
from aptos_sdk.bcs import Serializer
from aptos_sdk.client import ResourceNotFound
from aptos_sdk.transactions import TransactionArgument, EntryFunction, TransactionPayload
from aptos_sdk.type_tag import TypeTag, StructTag

from aptos.RestClientWithProxy import RestClientWithProxy
from aptos.token_addresses import TOKENS, STABLES


class LiquidSwap:
    aptos_uncorrelated = "0x190d44266241744264b964a37b8f09863167a12d3e70cda39376cfb4e3561e12::curves::Uncorrelated"
    __router_address = "0x190d44266241744264b964a37b8f09863167a12d3e70cda39376cfb4e3561e12"
    aptos_address = "0x1::aptos_coin::AptosCoin"
    liquidity_address = "0x05a97986a9d031c4567e15b797be516910cfcb4156312482efc6a19c0a30c948"

    def __init__(self, private_key: str, node: str = "https://rpc.ankr.com/http/aptos/v1", proxy: str = None,
                 slippage_tolerance: int | float = 1, user_agent: str = None, logger: logging.Logger = None):
        self.logger = logger
        self.node_url = node
        self.rest_client = RestClientWithProxy(node, proxy={'http': proxy, 'https': proxy},
                                               user_agent=user_agent, logger=self.logger)
        self.rest_client.client_config.max_gas_amount = 10000
        self.account = Account.load_key(private_key)
        self.slippage = slippage_tolerance

    def register_coin(self, token):
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
        to_token_balance_before_simulate = int(self.rest_client.account_resource(
                self.account.address(), f"0x1::coin::CoinStore<{to_token}>")["data"]["coin"]["value"])
        signed_tx = self.rest_client.create_bcs_transaction(
            self.account, TransactionPayload(payload)
        )

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
        curve_type = self.aptos_uncorrelated
        if (from_token in STABLES) and (to_token in STABLES):
            curve_type = "0x190d44266241744264b964a37b8f09863167a12d3e70cda39376cfb4e3561e12::curves::Stable"

        decimals_from = Decimal(
            self.rest_client.account_resource(
                from_token.split("::")[0], f"0x1::coin::CoinInfo<{from_token}>")["data"]["decimals"])
        try:
            self.rest_client.account_resource(self.account.address(), f"0x1::coin::CoinStore<{to_token}>")
        except ResourceNotFound:
            self.logger.warning("I never received this coin. Adding to my wallet")
            self.register_coin(to_token)

        payload = EntryFunction.natural(
            f"{self.__router_address}::scripts_v2",
            "swap",
            [
                TypeTag(StructTag.from_str(from_token)),
                TypeTag(StructTag.from_str(to_token)),
                TypeTag(StructTag.from_str(curve_type))
            ],
            [
                TransactionArgument(int(amount * (10 ** decimals_from)), Serializer.u64),
                TransactionArgument(0, Serializer.u64),
            ]
        )
        min_amount = self.__estimate_output(payload, to_token)
        if min_amount < 0:
            raise ValueError("Cannot estimate minimal amount for swap on LiquidSwap")
        payload = EntryFunction.natural(
            f"{self.__router_address}::scripts_v2",
            "swap",
            [
                TypeTag(StructTag.from_str(from_token)),
                TypeTag(StructTag.from_str(to_token)),
                TypeTag(StructTag.from_str(curve_type))
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

        pool_data = self.rest_client.account_resource(
            self.liquidity_address,
            f"{self.__router_address}::liquidity_pool::LiquidityPool"
            f"<{token},{self.aptos_address},{self.aptos_uncorrelated}>")
        exchange_rate = (Decimal(pool_data["data"]["coin_x_reserve"]["value"]) / (10 ** decimals_token)) / (
                    Decimal(pool_data["data"]["coin_y_reserve"]["value"]) / (10 ** decimals_apt))
        need_apt_amount = int((amount / exchange_rate) * 10 ** decimals_apt)
        need_token_amount = int(amount * (10 ** decimals_token))
        apt_amount_with_slippage = int((need_apt_amount / 100) * 98)
        token_amount_with_slippage = int((need_token_amount / 100) * 98)

        payload = EntryFunction.natural(
            f"{self.__router_address}::scripts_v2",
            "add_liquidity",
            [
                TypeTag(StructTag.from_str(token)),
                TypeTag(StructTag.from_str(self.aptos_address)),
                TypeTag(StructTag.from_str(
                    self.aptos_uncorrelated))
            ],
            [
                TransactionArgument(need_token_amount, Serializer.u64),
                TransactionArgument(token_amount_with_slippage, Serializer.u64),
                TransactionArgument(need_apt_amount, Serializer.u64),
                TransactionArgument(apt_amount_with_slippage, Serializer.u64)
            ]
        )
        signed_tx = self.rest_client.create_bcs_signed_transaction(self.account, TransactionPayload(payload))
        return self.rest_client.submit_bcs_transaction(signed_tx)

    def remove_liquidity_for_apt(self, token: str, amount_liquidity: Decimal | int) -> str:
        supply_amount = Decimal(self.rest_client.account_resource(
            self.liquidity_address,
            f"0x1::coin::CoinInfo<{self.liquidity_address}::lp_coin::LP<{token},{self.aptos_address},"
            f"{self.aptos_uncorrelated}>>")["data"]["supply"]["vec"][0]["integer"]["vec"][0]["value"])
        pool_percent = Decimal(amount_liquidity) / Decimal(supply_amount)

        pool_data = self.rest_client.account_resource(
            self.liquidity_address,
            f"{self.__router_address}::liquidity_pool::LiquidityPool<{token},"
            f"{self.aptos_address},{self.aptos_uncorrelated}>")
        token_x = Decimal(pool_data["data"]["coin_x_reserve"]["value"]) * pool_percent
        token_y = Decimal(pool_data["data"]["coin_y_reserve"]["value"]) * pool_percent
        token_x_minus_slippage = int(token_x / 100 * 99)
        token_y_minus_slippage = int(token_y / 100 * 99)
        payload = EntryFunction.natural(
            f"{self.__router_address}::scripts_v2",
            "remove_liquidity",
            [
                TypeTag(StructTag.from_str(token)),
                TypeTag(StructTag.from_str(self.aptos_address)),
                TypeTag(StructTag.from_str(
                    self.aptos_uncorrelated))
            ],
            [
                TransactionArgument(int(amount_liquidity), Serializer.u64),
                TransactionArgument(token_x_minus_slippage, Serializer.u64),
                TransactionArgument(token_y_minus_slippage, Serializer.u64),
            ]
        )
        signed_tx = self.rest_client.create_bcs_signed_transaction(self.account, TransactionPayload(payload))
        return self.rest_client.submit_bcs_transaction(signed_tx)

    def exchange_with_amount_in_percent(self, percent: Decimal, route: str, save_apt_amount: int | Decimal = 0) -> str:
        token_from, token_to = TOKENS[route[0]], TOKENS[route[1]]
        decimals_from = Decimal(self.rest_client.account_resource(
            token_from.split("::")[0], f"0x1::coin::CoinInfo<{token_from}>")["data"]["decimals"])
        if route[0] == "APT":
            token_balance = save_apt_amount if save_apt_amount > 0 else Decimal(
                self.rest_client.account_resource(
                    self.account.address(), f"0x1::coin::CoinStore<{token_from}>")["data"]["coin"]["value"])
        else:
            token_balance = Decimal(self.rest_client.account_resource(
                self.account.address(), f"0x1::coin::CoinStore<{token_from}>")["data"]["coin"]["value"])
        swap_amount = Decimal(int((token_balance / 100)*percent))
        return self.swap(swap_amount / (10 ** decimals_from), token_from, token_to)

    def add_in_pool_for_apt_with_amount_in_percent(self, token, percent) -> str | None:
        decimals_from = Decimal(self.rest_client.account_resource(
            TOKENS[token].split("::")[0], f"0x1::coin::CoinInfo<{TOKENS[token]}>")["data"]["decimals"])
        try:
            token_balance = Decimal(self.rest_client.account_resource(
                self.account.address(), f"0x1::coin::CoinStore<{TOKENS[token]}>")["data"]["coin"]["value"])
        except ResourceNotFound:
            token_balance = 0

        if token_balance == 0:
            self.logger.warning(f"We cannot invest to {token}/APT to liquidswap")
            return None

        swap_amount = Decimal(int((token_balance / 100) * percent))
        return self.add_liquidity_for_apt(TOKENS[token], swap_amount/(10 ** decimals_from))

    def remove_from_pool_for_apt_with_amount_in_percent(self, token, percent):
        try:
            token_balance = Decimal(self.rest_client.account_resource(
                self.account.address(),
                f"0x1::coin::CoinStore<{self.liquidity_address}::lp_coin::LP<{TOKENS[token]},"
                f"{self.aptos_address},{self.aptos_uncorrelated}>>")["data"]["coin"]["value"])
        except:
            self.logger.warning(f"We dont invest to pool {token}/APT on liquidswap")
            return None

        if token_balance == 0:
            self.logger.warning(f"We dont invest to pool {token}/APT on liquidswap")
            return None

        remove_liquidity_amount = int(token_balance / 100 * percent)
        return self.remove_liquidity_for_apt(TOKENS[token], remove_liquidity_amount)

    def get_transaction_status(self, tx: str | None) -> bool:
        if tx is None:
            return True
        try:
            self.rest_client.wait_for_transaction(tx)
            return True
        except AssertionError:
            return False
