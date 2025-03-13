from layerzero.network.network import EVMNetwork
from layerzero.network.coredao.constants import CoredaoConstants
from layerzero.network.stablecoin import Stablecoin
from layerzero.stargate import StargateConstants


class Coredao(EVMNetwork):

    def __init__(self):
        supported_stablecoins = {
            'USDT': Stablecoin('USDT', CoredaoConstants.USDT_CONTRACT_ADDRESS, CoredaoConstants.USDT_DECIMALS,
                               CoredaoConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDT']),
        }

        super().__init__(CoredaoConstants.NAME, CoredaoConstants.NATIVE_TOKEN, CoredaoConstants.RPC,
                         CoredaoConstants.STARGATE_CHAIN_ID, CoredaoConstants.STARGATE_ROUTER_CONTRACT_ADDRESS,
                         CoredaoConstants.STARGATE_ROUTER_ETH_CONTRACT_ADDRESS,
                         supported_stablecoins, CoredaoConstants.STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS,
                         CoredaoConstants.MERKLY_CONTRACT_ADDRESS, CoredaoConstants.MERKLY_MAX_TRANSFER,
                         CoredaoConstants.MERKLY_NETWORKS)

    def _get_approve_gas_limit(self) -> int:
        return CoredaoConstants.APPROVE_GAS_LIMIT
