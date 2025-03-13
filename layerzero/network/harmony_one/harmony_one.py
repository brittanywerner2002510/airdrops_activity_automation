from layerzero.network.network import EVMNetwork
from layerzero.network.harmony_one.constants import HarmonyConstants
from layerzero.network.stablecoin import Stablecoin
from layerzero.stargate import StargateConstants


class Harmony(EVMNetwork):

    def __init__(self):
        supported_stablecoins = {
            'USDT': Stablecoin('USDT', HarmonyConstants.USDT_CONTRACT_ADDRESS, HarmonyConstants.USDT_DECIMALS,
                               HarmonyConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDT']),
            'USDC': Stablecoin('USDC', HarmonyConstants.USDC_CONTRACT_ADDRESS, HarmonyConstants.USDC_DECIMALS,
                               HarmonyConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDC'])
        }

        super().__init__(HarmonyConstants.NAME, HarmonyConstants.NATIVE_TOKEN, HarmonyConstants.RPC,
                         HarmonyConstants.STARGATE_CHAIN_ID, HarmonyConstants.STARGATE_ROUTER_CONTRACT_ADDRESS,
                         HarmonyConstants.STARGATE_ROUTER_ETH_CONTRACT_ADDRESS,
                         supported_stablecoins, HarmonyConstants.STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS,
                         HarmonyConstants.MERKLY_CONTRACT_ADDRESS, HarmonyConstants.MERKLY_MAX_TRANSFER,
                         HarmonyConstants.MERKLY_NETWORKS)

    def _get_approve_gas_limit(self) -> int:
        return HarmonyConstants.APPROVE_GAS_LIMIT
