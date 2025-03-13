from layerzero.network.network import EVMNetwork
from layerzero.network.optimism.constants import OptimismConstants
from layerzero.network.stablecoin import Stablecoin
from layerzero.stargate import StargateConstants


class Optimism(EVMNetwork):

    def __init__(self):
        supported_stablecoins = {
            'USDC': Stablecoin('USDC', OptimismConstants.USDC_CONTRACT_ADDRESS, OptimismConstants.USDC_DECIMALS,
                               OptimismConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDC']),
            'ETH': Stablecoin('ETH', OptimismConstants.ETH_CONTRACT_ADDRESS, OptimismConstants.ETH_DECIMALS,
                              OptimismConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['ETH'])
        }

        super().__init__(OptimismConstants.NAME, OptimismConstants.NATIVE_TOKEN, OptimismConstants.RPC,
                         OptimismConstants.STARGATE_CHAIN_ID, OptimismConstants.STARGATE_ROUTER_CONTRACT_ADDRESS,
                         OptimismConstants.STARGATE_ROUTER_ETH_CONTRACT_ADDRESS,
                         supported_stablecoins, OptimismConstants.STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS,
                         OptimismConstants.MERKLY_CONTRACT_ADDRESS, OptimismConstants.MERKLY_MAX_TRANSFER,
                         OptimismConstants.MERKLY_NETWORKS)

    def _get_approve_gas_limit(self) -> int:
        return OptimismConstants.APPROVE_GAS_LIMIT
