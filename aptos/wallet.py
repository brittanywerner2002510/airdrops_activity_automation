import logging
from decimal import Decimal

from aptos_sdk.account import Account
from aptos_sdk.account_address import AccountAddress
from aptos_sdk.bcs import Serializer
from aptos_sdk.client import ResourceNotFound
from aptos_sdk.client import RestClient
from aptos_sdk.transactions import TransactionArgument, EntryFunction, TransactionPayload

from aptos.RestClientWithProxy import RestClientWithProxy


class Wallet:
    def __init__(self, pk: str, node: str = "https://rpc.ankr.com/http/aptos/v1", proxy: dict = None,
                 user_agent: str = None, logger: logging.Logger = None):
        self.logger = logger or logging
        if proxy is not None:
            self.rest_client = RestClientWithProxy(node, proxy={'http': proxy, 'https': proxy},
                                                   user_agent=user_agent, logger=self.logger)
        else:
            self.rest_client = RestClient(node)
        self.account = Account.load_key(pk)
        self.default_gas_limit = self.rest_client.client_config.max_gas_amount
        self.custom_gas_limit = 1000
        self.node = node

    def calculate_max_transfer_amount(self, address: str) -> Decimal:
        balance = self.rest_client.account_balance(self.account.address())
        if int(balance) < 0.1 * 10 ** 8:
            self.rest_client.client_config.max_gas_amount = self.custom_gas_limit
        else:
            self.rest_client.client_config.max_gas_amount = 100_000
        transaction_arguments = [
            TransactionArgument(AccountAddress.from_hex(address), Serializer.struct),
            TransactionArgument(1, Serializer.u64)
        ]
        payload = EntryFunction.natural(
            "0x1::aptos_account",
            "transfer",
            [],
            transaction_arguments,
        )

        signed_transaction = self.rest_client.create_bcs_transaction(
            self.account, TransactionPayload(payload))
        tx_info = self.rest_client.simulate_transaction(signed_transaction, self.account)[0]
        if not tx_info["success"]:
            raise RuntimeError(f"Error while estimate tx: {tx_info['vm_status']}")
        self.logger.info(tx_info)
        self.logger.info(Decimal(tx_info["gas_used"]) * Decimal(tx_info["gas_unit_price"]))
        max_amount = Decimal(balance) - (Decimal(tx_info["gas_used"]) * Decimal(tx_info["gas_unit_price"]))
        return max_amount

    def transfer(self, address: str, amount: Decimal) -> str:
        transaction_arguments = [
            TransactionArgument(AccountAddress.from_hex(address), Serializer.struct),
            TransactionArgument(int(amount), Serializer.u64),
        ]

        payload = EntryFunction.natural(
            "0x1::aptos_account",
            "transfer",
            [],
            transaction_arguments,
        )

        signed_transaction = self.rest_client.create_bcs_signed_transaction(
            self.account, TransactionPayload(payload)
        )
        tx_info = self.rest_client.submit_bcs_transaction(signed_transaction)
        return tx_info

    def get_public_key(self) -> str:
        return str(self.account.address())

    def get_native_token_amount(self) -> Decimal:
        try:
            return Decimal(self.rest_client.account_resource(self.account.address(),
                                                             f"0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>")[
                               "data"]["coin"]["value"])
        except ResourceNotFound:
            logging.warning("Resource not found... may be this address new?")
            return Decimal("0")

    def get_token_amount(self, token):
        try:
            return Decimal(
                self.rest_client.account_resource(self.account.address(),
                                                  f"0x1::coin::CoinStore<{token}>")["data"]["coin"]["value"])
        except ResourceNotFound:
            return 0

    def get_transaction_status(self, tx: str) -> bool:
        if tx is None:
            return True
        try:
            self.rest_client.wait_for_transaction(tx)
            return True
        except AssertionError:
            return False
