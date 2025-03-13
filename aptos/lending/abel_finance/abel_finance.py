import logging
from decimal import Decimal

from aptos_sdk.account import Account
from aptos_sdk.bcs import Serializer
from aptos_sdk.transactions import TransactionArgument, EntryFunction, TransactionPayload
from aptos_sdk.type_tag import TypeTag, StructTag

from aptos.RestClientWithProxy import RestClientWithProxy


class AbelFinance:
    abel_finance_token = ("0xc0188ad3f42e66b5bd3596e642b8f72749b67d84e6349ce325b27117a9406bdf:"
                          ":acoin::ACoinStore<0x1::aptos_coin::AptosCoin>")
    aptos_coin = "0x1::aptos_coin::AptosCoin"

    def __init__(self, private_key: str, node: str = "https://rpc.ankr.com/http/aptos/v1", proxy: str = None,
                 user_agent: str = None, logger: logging.Logger = None):
        self.logger = logger
        self.node_url = node
        self.rest_client = RestClientWithProxy(node, proxy={'http': proxy, 'https': proxy}, user_agent=user_agent,
                                               logger=self.logger)
        self.rest_client.client_config.max_gas_amount = 10000
        self.account = Account.load_key(private_key)
        self.lending_address = "0xc0188ad3f42e66b5bd3596e642b8f72749b67d84e6349ce325b27117a9406bdf"
        self.min_apt_amount = Decimal("0")

    def deposit(self, amount: Decimal) -> str:
        payload = EntryFunction.natural(
            f"{self.lending_address}::acoin_lend",
            "mint_entry",
            [
                TypeTag(StructTag.from_str(self.aptos_coin)),
            ],
            [
                TransactionArgument(int(amount), Serializer.u64),
            ]
        )
        signed_tx = self.rest_client.create_bcs_signed_transaction(self.account, TransactionPayload(payload))
        sim_tx = self.rest_client.create_bcs_transaction(self.account, TransactionPayload(payload))
        tx_info = self.rest_client.simulate_transaction(sim_tx, self.account)[0]
        if tx_info["success"]:
            return self.rest_client.submit_bcs_transaction(signed_tx)
        else:
            self.logger.error("Simulation transaction failed :(")
            raise RuntimeError(tx_info)

    def withdraw(self, amount: Decimal) -> str:
        payload = EntryFunction.natural(
            f"{self.lending_address}::acoin_lend",
            "redeem_entry",
            [
                TypeTag(StructTag.from_str(self.aptos_coin)),
            ],
            [
                TransactionArgument(int(amount), Serializer.u64),
            ]
        )
        signed_tx = self.rest_client.create_bcs_signed_transaction(self.account, TransactionPayload(payload))
        sim_tx = self.rest_client.create_bcs_transaction(self.account, TransactionPayload(payload))
        tx_info = self.rest_client.simulate_transaction(sim_tx, self.account)[0]
        if tx_info["success"]:
            return self.rest_client.submit_bcs_transaction(signed_tx)
        else:
            self.logger.error("Simulation transaction failed")
            raise RuntimeError(tx_info)

    def deposit_safe(self, amount: Decimal) -> str:
        aptos_decimals = Decimal(self.rest_client.account_resource(
            self.aptos_coin.split("::")[0], f"0x1::coin::CoinInfo<{self.aptos_coin}>")["data"]["decimals"])

        if amount * 10 ** aptos_decimals >= self.min_apt_amount * 10 ** aptos_decimals:
            return self.deposit(amount * 10 ** aptos_decimals)
        else:
            raise RuntimeError("Less than min allowed")

    def withdraw_safe(self, amount: Decimal) -> str:
        token_amount = Decimal(
            self.rest_client.account_resource(self.account.address(),
                                              f"{self.abel_finance_token}")["data"]["coin"]["value"])
        aptos_decimals = Decimal(self.rest_client.account_resource(
            self.aptos_coin.split("::")[0], f"0x1::coin::CoinInfo<{self.aptos_coin}>")["data"]["decimals"])

        if amount == "100%":
            return self.withdraw(token_amount)
        else:
            return self.withdraw(amount * 10 ** aptos_decimals)
