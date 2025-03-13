from layerzero.network.network import EVMNetwork
from layerzero.network.kava.constants import KavaConstants
from layerzero.network.stablecoin import Stablecoin
from layerzero.stargate import StargateConstants


class Kava(EVMNetwork):

    def __init__(self):
        supported_stablecoins = {
            'USDT': Stablecoin('USDT', KavaConstants.USDT_CONTRACT_ADDRESS, KavaConstants.USDT_DECIMALS,
                               KavaConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDT'])
        }

        super().__init__(KavaConstants.NAME, KavaConstants.NATIVE_TOKEN, KavaConstants.RPC,
                         KavaConstants.STARGATE_CHAIN_ID, KavaConstants.STARGATE_ROUTER_CONTRACT_ADDRESS,
                         KavaConstants.STARGATE_ROUTER_ETH_CONTRACT_ADDRESS,
                         supported_stablecoins, KavaConstants.STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS,
                         KavaConstants.MERKLY_CONTRACT_ADDRESS, KavaConstants.MERKLY_MAX_TRANSFER,
                         KavaConstants.MERKLY_NETWORKS)

    def _get_approve_gas_limit(self) -> int:
        return KavaConstants.APPROVE_GAS_LIMIT
