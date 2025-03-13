from layerzero.network.network import EVMNetwork
from layerzero.network.base.constants import BaseConstants
from layerzero.network.stablecoin import Stablecoin
from layerzero.stargate import StargateConstants


class Base(EVMNetwork):

    def __init__(self):
        supported_stablecoins = {
            'ETH': Stablecoin('ETH', BaseConstants.ETH_CONTRACT_ADDRESS, BaseConstants.ETH_DECIMALS,
                              BaseConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['ETH']),
            'USDC': Stablecoin('USDC', BaseConstants.USDC_CONTRACT_ADDRESS, BaseConstants.USDC_DECIMALS,
                               BaseConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDC'])
        }

        super().__init__(BaseConstants.NAME, BaseConstants.NATIVE_TOKEN, BaseConstants.RPC,
                         BaseConstants.STARGATE_CHAIN_ID, BaseConstants.STARGATE_ROUTER_CONTRACT_ADDRESS,
                         BaseConstants.STARGATE_ROUTER_ETH_CONTRACT_ADDRESS,
                         supported_stablecoins, BaseConstants.STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS,
                         BaseConstants.MERKLY_CONTRACT_ADDRESS, BaseConstants.MERKLY_MAX_TRANSFER,
                         BaseConstants.MERKLY_NETWORKS)

    def _get_approve_gas_limit(self) -> int:
        return BaseConstants.APPROVE_GAS_LIMIT
