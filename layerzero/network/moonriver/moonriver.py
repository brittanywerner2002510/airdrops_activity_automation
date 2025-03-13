from layerzero.network.network import EVMNetwork
from layerzero.network.moonriver.constants import MoonriverConstants
from layerzero.network.stablecoin import Stablecoin
from layerzero.stargate import StargateConstants


class Moonriver(EVMNetwork):

    def __init__(self):
        supported_stablecoins = {
            'USDT': Stablecoin('USDT', MoonriverConstants.USDT_CONTRACT_ADDRESS, MoonriverConstants.USDT_DECIMALS,
                               MoonriverConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDT']),
            'USDC': Stablecoin('USDC', MoonriverConstants.USDC_CONTRACT_ADDRESS, MoonriverConstants.USDC_DECIMALS,
                               MoonriverConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDC'])
        }

        super().__init__(MoonriverConstants.NAME, MoonriverConstants.NATIVE_TOKEN, MoonriverConstants.RPC,
                         MoonriverConstants.STARGATE_CHAIN_ID, MoonriverConstants.STARGATE_ROUTER_CONTRACT_ADDRESS,
                         MoonriverConstants.STARGATE_ROUTER_ETH_CONTRACT_ADDRESS,
                         supported_stablecoins, MoonriverConstants.STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS,
                         MoonriverConstants.MERKLY_CONTRACT_ADDRESS, MoonriverConstants.MERKLY_MAX_TRANSFER,
                         MoonriverConstants.MERKLY_NETWORKS)

    def _get_approve_gas_limit(self) -> int:
        return MoonriverConstants.APPROVE_GAS_LIMIT
