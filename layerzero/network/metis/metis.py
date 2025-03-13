from layerzero.network.network import EVMNetwork
from layerzero.network.metis.constants import MetisConstants
from layerzero.network.stablecoin import Stablecoin
from layerzero.stargate import StargateConstants


class Metis(EVMNetwork):

    def __init__(self):
        supported_stablecoins = {
            'm.USDT': Stablecoin('m.USDT', MetisConstants.m_USDT_CONTRACT_ADDRESS, MetisConstants.USDT_DECIMALS,
                                 MetisConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['m.USDT']),
        }

        super().__init__(MetisConstants.NAME, MetisConstants.NATIVE_TOKEN, MetisConstants.RPC,
                         MetisConstants.STARGATE_CHAIN_ID, MetisConstants.STARGATE_ROUTER_CONTRACT_ADDRESS,
                         MetisConstants.STARGATE_ROUTER_ETH_CONTRACT_ADDRESS,
                         supported_stablecoins, MetisConstants.STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS,
                         MetisConstants.MERKLY_CONTRACT_ADDRESS, MetisConstants.MERKLY_MAX_TRANSFER,
                         MetisConstants.MERKLY_NETWORKS)

    def _get_approve_gas_limit(self) -> int:
        return MetisConstants.APPROVE_GAS_LIMIT
