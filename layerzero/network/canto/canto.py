from layerzero.network.network import EVMNetwork
from layerzero.network.canto.constants import CantoConstants
from layerzero.network.stablecoin import Stablecoin
from layerzero.stargate import StargateConstants


class Canto(EVMNetwork):

    def __init__(self):
        supported_stablecoins = {
            'USDT': Stablecoin('USDT', CantoConstants.USDT_CONTRACT_ADDRESS, CantoConstants.USDT_DECIMALS,
                               CantoConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDT']),
            'USDC': Stablecoin('USDC', CantoConstants.USDC_CONTRACT_ADDRESS, CantoConstants.USDC_DECIMALS,
                               CantoConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDC'])
        }

        super().__init__(CantoConstants.NAME, CantoConstants.NATIVE_TOKEN, CantoConstants.RPC,
                         CantoConstants.STARGATE_CHAIN_ID, CantoConstants.STARGATE_ROUTER_CONTRACT_ADDRESS,
                         CantoConstants.STARGATE_ROUTER_ETH_CONTRACT_ADDRESS,
                         supported_stablecoins, CantoConstants.STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS,
                         CantoConstants.MERKLY_CONTRACT_ADDRESS, CantoConstants.MERKLY_MAX_TRANSFER,
                         CantoConstants.MERKLY_NETWORKS)

    def _get_approve_gas_limit(self) -> int:
        return CantoConstants.APPROVE_GAS_LIMIT
