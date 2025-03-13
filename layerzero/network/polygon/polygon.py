from layerzero.network.network import EVMNetwork
from layerzero.network.polygon.constants import PolygonConstants
from layerzero.network.stablecoin import Stablecoin
from layerzero.stargate import StargateConstants


class Polygon(EVMNetwork):

    def __init__(self):
        supported_stablecoins = {
            'USDT': Stablecoin('USDT', PolygonConstants.USDT_CONTRACT_ADDRESS, PolygonConstants.USDC_DECIMALS,
                               PolygonConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDT']),
            'USDC': Stablecoin('USDC', PolygonConstants.USDC_CONTRACT_ADDRESS, PolygonConstants.USDC_DECIMALS,
                               PolygonConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDC'])
        }

        super().__init__(PolygonConstants.NAME, PolygonConstants.NATIVE_TOKEN, PolygonConstants.RPC,
                         PolygonConstants.STARGATE_CHAIN_ID, PolygonConstants.STARGATE_ROUTER_CONTRACT_ADDRESS,
                         PolygonConstants.STARGATE_ROUTER_ETH_CONTRACT_ADDRESS,
                         supported_stablecoins, PolygonConstants.STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS,
                         PolygonConstants.MERKLY_CONTRACT_ADDRESS, PolygonConstants.MERKLY_MAX_TRANSFER,
                         PolygonConstants.MERKLY_NETWORKS, PolygonConstants.NATIVE_DECIMALS)

    def _get_approve_gas_limit(self) -> int:
        return PolygonConstants.APPROVE_GAS_LIMIT
