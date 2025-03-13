import logging
from decimal import Decimal

from aptos_sdk.account import Account
from aptos_sdk.bcs import Serializer
from aptos_sdk.client import ResourceNotFound
from aptos_sdk.transactions import TransactionArgument, EntryFunction, TransactionPayload
from aptos_sdk.type_tag import TypeTag, StructTag

from aptos.RestClientWithProxy import RestClientWithProxy


class Aptin:
    pool_position = "0xb7d960e5f0a58cc0817774e611d7e3ae54c6843816521f02d7ced583d6434896::pool::Positions"
    pool_supply_position = "0xb7d960e5f0a58cc0817774e611d7e3ae54c6843816521f02d7ced583d6434896::pool::SupplyPosition"
    aptos_coin = "0x1::aptos_coin::AptosCoin"

    def __init__(self, private_key: str, node: str = "https://rpc.ankr.com/http/aptos/v1",
                 proxy: str = None, user_agent: str = None, logger: logging.Logger = None):
        self.logger = logger
        self.node_url = node
        self.rest_client = RestClientWithProxy(node, proxy={'http': proxy, 'https': proxy}, user_agent=user_agent,
                                               logger=self.logger)
        self.rest_client.client_config.max_gas_amount = 10000
        self.account = Account.load_key(private_key)
        self.lending_address = "0xb7d960e5f0a58cc0817774e611d7e3ae54c6843816521f02d7ced583d6434896"
        self.min_apt_amount = Decimal("1")

    def get_position_amount(self) -> Decimal:
        position = self.rest_client.account_resource(self.account.address(), self.pool_position)
        position_info = self.rest_client.get_table_item(handle=position["data"]["supply_position"]["handle"],
                                                        key=self.aptos_coin,
                                                        key_type="0x1::string::String",
                                                        value_type=self.pool_supply_position)
        return Decimal(position_info["amount"])

    def deposit(self, amount: Decimal) -> str:
        payload = EntryFunction.natural(
            f"{self.lending_address}::lend",
            "supply",
            [
                TypeTag(StructTag.from_str(self.aptos_coin)),
            ],
            [
                TransactionArgument(int(amount), Serializer.u64),
                TransactionArgument(True, Serializer.bool),
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
            f"{self.lending_address}::lend",
            "withdraw",
            [
                TypeTag(StructTag.from_str(self.aptos_coin)),
            ],
            [
                TransactionArgument(int(amount), Serializer.u64),
                TransactionArgument(self.account.address(), Serializer.struct),
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
            self.aptos_coin.split("::")[0], f"0x1::coin::CoinInfo<{self.aptos_coin}>")["data"]["decimals"])
        if amount * 10 ** aptos_decimals >= self.min_apt_amount * 10 ** aptos_decimals:
            return self.deposit(amount * 10 ** aptos_decimals)
        else:
            raise RuntimeError("Less than min allowed")

    def withdraw_safe(self, amount: Decimal) -> str:
        aptos_decimals = Decimal(self.rest_client.account_resource(
            self.aptos_coin.split("::")[0], f"0x1::coin::CoinInfo<{self.aptos_coin}>")["data"]["decimals"])
        try:
            position_amount = self.get_position_amount()
        except ResourceNotFound:
            raise RuntimeError("Position not found")
        if amount == "100%":
            return self.withdraw(position_amount)
        elif Decimal(amount) * 10 ** aptos_decimals > position_amount:
            return self.withdraw(amount * 10 ** aptos_decimals)
