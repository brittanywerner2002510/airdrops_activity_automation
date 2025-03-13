import time

from layerzero.config import TimeRanges
from layerzero.network import EVMNetwork, Stablecoin
from eth_account.signers.local import LocalAccount
from layerzero.network.balance_helper import BalanceHelper


class BridgeHelper:

    def __init__(self, account: LocalAccount, balance_helper: BalanceHelper,
                 src_network: EVMNetwork, dst_network: EVMNetwork, src_stable_coin: Stablecoin,
                 dst_stable_coin: Stablecoin, amount: int, slippage: int):
        self.account = account
        self.balance_helper = balance_helper
        self.src_network = src_network
        self.dst_network = dst_network
        self.src_stable_coin = src_stable_coin
        self.dst_stable_coin = dst_stable_coin
        self.amount = amount
        self.slippage = slippage

    def _is_bridge_possible(self) -> bool:
        if not self.balance_helper.is_enough_native_token_balance_for_stargate_swap_fee(self.dst_network):
            return False

        stable_coin_balance = self.src_network.get_token_balance(self.src_stable_coin.contract_address,
                                                                 self.account.address)
        if stable_coin_balance < self.amount:
            return False
        return True

    def approve_stablecoin_usage(self, amount: int) -> None:
        allowance = self.src_network.get_token_allowance(self.src_stable_coin.contract_address, self.account.address,
                                                         self.src_network.stargate_router_address)
        if allowance < amount:
            self.src_network.approve_token_usage(self.account.key, self.src_stable_coin.contract_address,
                                                 self.src_network.stargate_router_address, amount)

    def make_bridge(self) -> bool:
        if not self._is_bridge_possible():
            return False
        self.approve_stablecoin_usage(self.amount)
        amount_with_slippage = self.amount - int(self.amount * self.slippage)
        time.sleep(TimeRanges.MINUTE)

        return self.src_network.make_stargate_swap(self.account.key, self.dst_network.stargate_chain_id,
                                                   self.src_stable_coin.stargate_pool_id,
                                                   self.dst_stable_coin.stargate_pool_id,
                                                   self.amount, amount_with_slippage)
