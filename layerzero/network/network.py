from typing import Dict

import web3.exceptions
from web3 import HTTPProvider, Web3

from layerzero.abi import (ERC20_ABI, STARGATE_ROUTER_ABI, STARGATE_LIBRARY_FEE_ABI,
                           ORIGINAL_TOKEN_BRIDGE_ABI, STARGATE_ETH_ABI)
from layerzero.errors.errors_types import NotSupported
from layerzero.network.stablecoin import Stablecoin
from layerzero.stargate import StargateConstants


class Network:

    def __init__(self, name: str, native_token: str, rpc: str, stargate_chain_id: int,
                 stargate_router_address: str, stargate_router_eth_address: str,
                 stargate_library_fee_address: str, merkly_address: str, merkly_max_transfer: str,
                 merkly_networks: list, native_decimals: int = 18):
        self.name = name
        self.native_token = native_token
        self.rpc = rpc
        self.stargate_chain_id = stargate_chain_id
        self.stargate_router_address = stargate_router_address
        self.stargate_router_eth_address = stargate_router_eth_address
        self.stargate_library_fee_address = stargate_library_fee_address
        self.merkly_address = merkly_address
        self.merkly_max_transfer = merkly_max_transfer
        self.merkly_networks = merkly_networks
        self.native_decimals = native_decimals

    def get_balance(self, address: str) -> int:
        raise NotSupported(f"{self.name} get_balance() is not implemented")

    def get_token_balance(self, contract_address: str, address: str) -> int:
        raise NotSupported(f"{self.name} get_token_balance() is not implemented")


class EVMNetwork(Network):

    def __init__(self, name: str, native_token: str, rpc: str,
                 stargate_chain_id: int, stargate_router_address: str, stargate_router_eth_address: str,
                 supported_stable_coins: Dict[str, Stablecoin], stargate_library_fee_address: str, merkly_address: str,
                 merkly_max_transfer: str, merkly_networks: list, native_decimals=18):
        super().__init__(name, native_token, rpc, stargate_chain_id, stargate_router_address,
                         stargate_router_eth_address, stargate_library_fee_address, merkly_address, merkly_max_transfer,
                         merkly_networks, native_decimals)
        self.w3 = Web3(HTTPProvider(rpc))
        self.supported_stable_coins = supported_stable_coins

    def get_balance(self, address: str) -> int:
        return self.w3.eth.get_balance(Web3.to_checksum_address(address))

    def get_current_gas(self) -> int:
        return self.w3.eth.gas_price

    def get_current_gas_eth(self) -> float:
        eth_gas_price = self.get_current_gas()
        return self.w3.from_wei(eth_gas_price, 'gwei')

    def get_nonce(self, address: str) -> int:
        return self.w3.eth.get_transaction_count(Web3.to_checksum_address(address))

    def get_token_balance(self, contract_address: str, address: str) -> int:
        contract = self.w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=ERC20_ABI)
        return contract.functions.balanceOf(Web3.to_checksum_address(address)).call()

    def get_token_allowance(self, contract_address: str, owner: str, spender: str) -> int:
        contract = self.w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=ERC20_ABI)
        return contract.functions.allowance(Web3.to_checksum_address(owner),
                                            Web3.to_checksum_address(spender)).call()

    def _get_approve_gas_limit(self) -> int:
        raise NotSupported(f"{self.name} _get_approve_gas_limit() is not implemented")

    def approve_token_usage(self, private_key: str, contract_address: str, spender: str, amount: int) -> bool:
        account = self.w3.eth.account.from_key(private_key)
        contract = self.w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=ERC20_ABI)
        tx = contract.functions.approve(spender, amount).build_transaction(
            {
                'from': account.address,
                'gas': self._get_approve_gas_limit(),
                'gasPrice': int(self.get_current_gas()),
                'nonce': self.get_nonce(account.address)
            }
        )
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        try:
            self.w3.eth.wait_for_transaction_receipt(tx_hash)
        except web3.exceptions.TimeExhausted:
            return False
        return True

    def estimate_swap_gas_price(self) -> int:
        approve_gas_limit = self._get_approve_gas_limit()
        overall_gas_limit = StargateConstants.SWAP_GAS_LIMIT[self.name] + approve_gas_limit
        gas_price = overall_gas_limit * self.get_current_gas()
        return gas_price

    def estimate_layerzero_swap_fee(self, dst_chain_id: int, dst_address: str, additional_amount: int = None) -> int:
        contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(self.stargate_router_address),
            abi=STARGATE_ROUTER_ABI)
        if additional_amount is None:
            quote_data = contract.functions.quoteLayerZeroFee(
                dst_chain_id,
                1,  # function type (1 - swap): see Bridge.sol for all types
                dst_address,
                "0x",  # payload, using abi.encode()
                [0,  # extra gas, if calling smart contract
                 0,  # amount of dust dropped in destination wallet
                 "0x"  # destination wallet for dust
                 ]
            ).call()
        else:
            quote_data = contract.functions.quoteLayerZeroFee(
                dst_chain_id,
                1,  # function type (1 - swap): see Bridge.sol for all types
                dst_address,
                "0x",  # payload, using abi.encode()
                [0,  # extra gas, if calling smart contract
                 additional_amount,  # amount of dust dropped in destination wallet
                 dst_address  # destination wallet for dust
                 ]
            ).call()
        return quote_data[0]

    def make_stargate_eth_swap(self, private_key: str, dst_chain_id: int, amount: int, min_received_amount: int,
                               native_token_amount: int = None, fast_gas: bool = False) -> tuple[bool, str] | bool:
        account = self.w3.eth.account.from_key(private_key)
        contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(self.stargate_router_eth_address),
            abi=STARGATE_ETH_ABI)
        layerzero_fee = self.estimate_layerzero_swap_fee(dst_chain_id, account.address, native_token_amount)
        nonce = self.get_nonce(account.address)
        gas_price = int(self.get_current_gas() * 1.2) if fast_gas else self.get_current_gas()

        tx = contract.functions.swapETH(
            dst_chain_id,
            account.address,
            account.address,
            amount,
            min_received_amount,
        ).build_transaction(
            {
                'from': account.address,
                'value': amount + layerzero_fee,
                'gas': StargateConstants.SWAP_GAS_LIMIT[self.name],
                'gasPrice': gas_price,
                'nonce': nonce
            }
        )
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        try:
            self.w3.eth.wait_for_transaction_receipt(tx_hash)
        except web3.exceptions.TimeExhausted:
            return False
        return True, tx_hash

    def make_stargate_swap(self, private_key: str, dst_chain_id: int, src_pool_id: int,
                           dst_pool_id: int, amount: int, min_received_amount: int,
                           native_token_amount: int = None, fast_gas: bool = False) -> tuple[bool, str] | bool:

        account = self.w3.eth.account.from_key(private_key)
        contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(self.stargate_router_address),
            abi=STARGATE_ROUTER_ABI)
        layerzero_fee = self.estimate_layerzero_swap_fee(dst_chain_id, account.address, native_token_amount)
        nonce = self.get_nonce(account.address)
        gas_price = int(self.get_current_gas() * 1.2) if fast_gas else self.get_current_gas()

        if native_token_amount is None:
            tx = contract.functions.swap(
                dst_chain_id,
                src_pool_id,
                dst_pool_id,
                account.address,
                amount,
                min_received_amount,
                [0,  # extra gas, if calling smart contract
                 0,  # amount of dust dropped in destination wallet
                 "0x"  # destination wallet for dust
                 ],
                account.address,
                "0x",  # "fee" is the native gas to pay for the cross chain message fee
            ).build_transaction(
                {
                    'from': account.address,
                    'value': layerzero_fee,
                    'gas': StargateConstants.SWAP_GAS_LIMIT[self.name],
                    'gasPrice': gas_price,
                    'nonce': nonce
                }
            )
        else:
            tx = contract.functions.swap(
                dst_chain_id,
                src_pool_id,
                dst_pool_id,
                account.address,
                amount,
                min_received_amount,
                [0,  # extra gas, if calling smart contract
                 native_token_amount,  # amount of dust dropped in destination wallet
                 account.address  # destination wallet for dust
                 ],
                account.address,
                "0x",  # "fee" is the native gas to pay for the cross chain message fee
            ).build_transaction(
                {
                    'from': account.address,
                    'value': layerzero_fee,
                    'gas': StargateConstants.SWAP_GAS_LIMIT[self.name],
                    'gasPrice': gas_price,
                    'nonce': nonce
                }
            )
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        try:
            self.w3.eth.wait_for_transaction_receipt(tx_hash)
        except web3.exceptions.TimeExhausted:
            return False
        return True, tx_hash

    def estimate_stargate_fees(self, src_pool_id: int, dst_pool_id: int,
                               dst_chain_id: int, address: str, amount: int, decimals: int) -> dict:
        contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(self.stargate_library_fee_address),
            abi=STARGATE_LIBRARY_FEE_ABI)
        if self.name == "BSC":
            stargate_fees = contract.functions.getFees(
                src_pool_id,
                dst_pool_id,
                dst_chain_id,
                address,
                amount
            ).call()
            fee_description = {
                "eq_fee": stargate_fees[1] / (10 ** decimals),
                "eq_reward": stargate_fees[2] / (10 ** decimals),
                "lp_fee": stargate_fees[3] / (10 ** decimals),
                "protocol_fee": stargate_fees[4] / (10 ** decimals),
                "sum_fee": (stargate_fees[1] - stargate_fees[2] + stargate_fees[3] + stargate_fees[4]) / (
                            10 ** decimals)
            }
            return fee_description
        stargate_fees = contract.functions.getFees(
            src_pool_id,
            dst_pool_id,
            dst_chain_id,
            address,
            amount
        ).call()
        fee_description = {
            "eq_fee": stargate_fees[1] / (10 ** decimals),
            "eq_reward": stargate_fees[2] / (10 ** decimals),
            "lp_fee": stargate_fees[3] / (10 ** decimals),
            "protocol_fee": stargate_fees[4] / (10 ** decimals),
            "sum_fee": (stargate_fees[1] - stargate_fees[2] + stargate_fees[3] + stargate_fees[4]) / (10 ** decimals)
        }
        return fee_description

    def core_dao(self, private_key: str, amount: int) -> bool:
        correct_amount = int(amount * 10 ** self.supported_stable_coins['USDT'].decimals)
        account = self.w3.eth.account.from_key(private_key)
        contract = self.w3.eth.contract(
            address=Web3.to_checksum_address('0x52e75D318cFB31f9A2EdFa2DFee26B161255B233'),
            abi=ORIGINAL_TOKEN_BRIDGE_ABI)
        self.approve_token_usage(private_key, self.supported_stable_coins['USDT'].contract_address,
                                 '0x52e75D318cFB31f9A2EdFa2DFee26B161255B233', correct_amount)
        nonce = self.get_nonce(account.address)
        gas_price = 2000000000
        tx = contract.functions.bridge(
            self.supported_stable_coins['USDT'].contract_address,
            correct_amount,
            account.address,
            [
                account.address,
                account.address
            ],
            ''.encode('utf-8')
        ).build_transaction(
            {
                'from': account.address,
                'value': int(0.0002 * 10 ** 18),
                'gas': StargateConstants.SWAP_GAS_LIMIT[self.name],
                'gasPrice': gas_price,
                'nonce': nonce
            }
        )
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        try:
            self.w3.eth.wait_for_transaction_receipt(tx_hash)
        except web3.exceptions.TimeExhausted:
            return False
        return True

    def transfer(self, private_key: str, to: str, amount: int, stable: Stablecoin) -> str:
        coin_contract = self.w3.eth.contract(stable.contract_address, abi=ERC20_ABI)
        wei_amount = amount
        account = self.w3.eth.account.from_key(private_key)
        nonce = self.get_nonce(account.address)
        gas_price = self.w3.eth.gas_price
        to = self.w3.to_checksum_address(to)

        tx = coin_contract.functions.transfer(
            to,
            wei_amount
        ).build_transaction(
            {
                "nonce": nonce,
                'gas': 0,
                'gasPrice': 0,
                'from': account.address
            }
        )
        estimated_gas = self.w3.eth.estimate_gas(tx)

        tx = coin_contract.functions.transfer(
            to,
            wei_amount
        ).build_transaction(
            {
                "nonce": nonce,
                'gas': estimated_gas,
                'gasPrice': gas_price,
                'from': account.address
            }
        )

        signed_txn = self.w3.eth.account.sign_transaction(tx, private_key=private_key)
        tx_token = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return tx_token
