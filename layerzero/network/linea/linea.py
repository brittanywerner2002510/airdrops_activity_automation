from layerzero.network.network import EVMNetwork
from layerzero.network.linea.constants import LineaConstants
from layerzero.network.stablecoin import Stablecoin
from layerzero.stargate import StargateConstants


class Linea(EVMNetwork):

    def __init__(self):
        supported_stablecoins = {
            'ETH': Stablecoin('ETH', LineaConstants.ETH_CONTRACT_ADDRESS, LineaConstants.ETH_DECIMALS,
                              LineaConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['ETH'])
        }

        super().__init__(LineaConstants.NAME, LineaConstants.NATIVE_TOKEN, LineaConstants.RPC,
                         LineaConstants.STARGATE_CHAIN_ID, LineaConstants.STARGATE_ROUTER_CONTRACT_ADDRESS,
                         LineaConstants.STARGATE_ROUTER_ETH_CONTRACT_ADDRESS,
                         supported_stablecoins, LineaConstants.STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS,
                         LineaConstants.MERKLY_CONTRACT_ADDRESS, LineaConstants.MERKLY_MAX_TRANSFER,
                         LineaConstants.MERKLY_NETWORKS)

    def _get_approve_gas_limit(self) -> int:
        return LineaConstants.APPROVE_GAS_LIMIT
