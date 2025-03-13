from layerzero.network.network import EVMNetwork
from layerzero.network.polygon_zkevm.constants import PolygonZKConstants
from layerzero.network.stablecoin import Stablecoin
from layerzero.stargate import StargateConstants


class PolygonZk(EVMNetwork):

    def __init__(self):
        supported_stablecoins = {
            'USDT': Stablecoin('USDT', PolygonZKConstants.USDT_CONTRACT_ADDRESS, PolygonZKConstants.USDT_DECIMALS,
                               PolygonZKConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDT']),
            'USDC': Stablecoin('USDC', PolygonZKConstants.USDC_CONTRACT_ADDRESS, PolygonZKConstants.USDC_DECIMALS,
                               PolygonZKConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDC'])
        }

        super().__init__(PolygonZKConstants.NAME, PolygonZKConstants.NATIVE_TOKEN, PolygonZKConstants.RPC,
                         PolygonZKConstants.STARGATE_CHAIN_ID, PolygonZKConstants.STARGATE_ROUTER_CONTRACT_ADDRESS,
                         PolygonZKConstants.STARGATE_ROUTER_ETH_CONTRACT_ADDRESS,
                         supported_stablecoins, PolygonZKConstants.STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS,
                         PolygonZKConstants.MERKLY_CONTRACT_ADDRESS, PolygonZKConstants.MERKLY_MAX_TRANSFER,
                         PolygonZKConstants.MERKLY_NETWORKS)

    def _get_approve_gas_limit(self) -> int:
        return PolygonZKConstants.APPROVE_GAS_LIMIT
