import logging
from decimal import Decimal

from aptos_sdk.account import Account
from aptos_sdk.bcs import Serializer
from aptos_sdk.transactions import TransactionArgument, EntryFunction, TransactionPayload
from aptos_sdk.type_tag import TypeTag, StructTag

from aptos.RestClientWithProxy import RestClientWithProxy


class Aries:
    def __init__(self, private_key: str, node: str = "https://rpc.ankr.com/http/aptos/v1", proxy: str = None,
                 user_agent: str = None, logger: logging.Logger = None):
        self.logger = logger
        self.node_url = node
        self.rest_client = RestClientWithProxy(node, proxy={'http': proxy, 'https': proxy}, user_agent=user_agent,
                                               logger=self.logger)
        self.rest_client.client_config.max_gas_amount = 10000
        self.account = Account.load_key(private_key)
        self.lending_address = "0x9770fa9c725cbd97eb50b2be5f7416efdfd1f1554beb0750d4dae4c64e860da3"
        self.min_apt_amount = Decimal("0")
        self.aptos_token = "0x1::aptos_coin::AptosCoin"

    def create_main_profile(self) -> str:
        payload = EntryFunction.natural(
            f"{self.lending_address}::controller",
            "register_user",
            [

            ],
            [
                TransactionArgument("Main Account", Serializer.str),
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

    def deposit(self, amount: Decimal) -> str:
        payload = EntryFunction.natural(
            f"{self.lending_address}::controller",
            "deposit",
            [
                TypeTag(StructTag.from_str("0x1::aptos_coin::AptosCoin")),
            ],
            [
                TransactionArgument("Main Account", Serializer.str),
                TransactionArgument(int(amount), Serializer.u64),
                TransactionArgument(False, Serializer.bool),
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

    def withdraw(self, amount: int | Decimal) -> str:
        payload = EntryFunction.natural(
            f"{self.lending_address}::controller",
            "withdraw",
            [
                TypeTag(StructTag.from_str("0x1::aptos_coin::AptosCoin")),
            ],
            [
                TransactionArgument("Main Account", Serializer.str),
                TransactionArgument(int(amount), Serializer.u64),
                TransactionArgument(False, Serializer.bool),
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

    def deposit_safe(self, amount: Decimal) -> str:
        aptos_decimals = Decimal(self.rest_client.account_resource(
            self.aptos_token.split("::")[0], f"0x1::coin::CoinInfo<{self.aptos_token}>")["data"]["decimals"])
        try:
            self.create_main_profile()
        except BaseException:
            self.logger.error("Something went wrong", exc_info=True)

        if amount * 10 ** aptos_decimals >= self.min_apt_amount * 10 ** aptos_decimals:
            return self.deposit(amount * 10 ** aptos_decimals)
        else:
            raise RuntimeError("Less than min allowed")

    def withdraw_safe(self, amount: str):
        if amount == "100%":
            return self.withdraw(18446744073709551615)
