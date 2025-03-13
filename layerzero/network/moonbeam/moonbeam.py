from layerzero.network.network import EVMNetwork
from layerzero.network.moonbeam.constants import MoonbeamConstants
from layerzero.network.stablecoin import Stablecoin
from layerzero.stargate import StargateConstants


class Moonbeam(EVMNetwork):

    def __init__(self):
        supported_stablecoins = {
            'USDT': Stablecoin('USDT', MoonbeamConstants.USDT_CONTRACT_ADDRESS, MoonbeamConstants.USDT_DECIMALS,
                               MoonbeamConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDT']),
            'USDC': Stablecoin('USDC', MoonbeamConstants.USDC_CONTRACT_ADDRESS, MoonbeamConstants.USDC_DECIMALS,
                               MoonbeamConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDC'])
        }

        super().__init__(MoonbeamConstants.NAME, MoonbeamConstants.NATIVE_TOKEN, MoonbeamConstants.RPC,
                         MoonbeamConstants.STARGATE_CHAIN_ID, MoonbeamConstants.STARGATE_ROUTER_CONTRACT_ADDRESS,
                         MoonbeamConstants.STARGATE_ROUTER_ETH_CONTRACT_ADDRESS,
                         supported_stablecoins, MoonbeamConstants.STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS,
                         MoonbeamConstants.MERKLY_CONTRACT_ADDRESS, MoonbeamConstants.MERKLY_MAX_TRANSFER,
                         MoonbeamConstants.MERKLY_NETWORKS)

    def _get_approve_gas_limit(self) -> int:
        return MoonbeamConstants.APPROVE_GAS_LIMIT
