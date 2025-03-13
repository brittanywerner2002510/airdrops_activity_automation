from layerzero.network.network import EVMNetwork
from layerzero.network.fantom.constants import FantomConstants
from layerzero.network.stablecoin import Stablecoin
from layerzero.stargate import StargateConstants


class Fantom(EVMNetwork):

    def __init__(self):
        supported_stablecoins = {
            'USDC': Stablecoin('USDC', FantomConstants.USDC_CONTRACT_ADDRESS, FantomConstants.USDC_DECIMALS,
                               FantomConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDC'])
        }

        super().__init__(FantomConstants.NAME, FantomConstants.NATIVE_TOKEN, FantomConstants.RPC,
                         FantomConstants.STARGATE_CHAIN_ID, FantomConstants.STARGATE_ROUTER_CONTRACT_ADDRESS,
                         FantomConstants.STARGATE_ROUTER_ETH_CONTRACT_ADDRESS,
                         supported_stablecoins, FantomConstants.STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS,
                         FantomConstants.MERKLY_CONTRACT_ADDRESS, FantomConstants.MERKLY_MAX_TRANSFER,
                         FantomConstants.MERKLY_NETWORKS, FantomConstants.NATIVE_DECIMALS)

    def _get_approve_gas_limit(self) -> int:
        return FantomConstants.APPROVE_GAS_LIMIT
