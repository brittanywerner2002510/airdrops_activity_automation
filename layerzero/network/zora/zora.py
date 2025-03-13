from layerzero.network.network import EVMNetwork
from layerzero.network.zora.constants import ZoraConstants
from layerzero.network.stablecoin import Stablecoin
from layerzero.stargate import StargateConstants


class Zora(EVMNetwork):

    def __init__(self):
        supported_stablecoins = {
            'USDT': Stablecoin('USDT', ZoraConstants.USDT_CONTRACT_ADDRESS, ZoraConstants.USDT_DECIMALS,
                               ZoraConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDT']),
            'USDC': Stablecoin('USDC', ZoraConstants.USDC_CONTRACT_ADDRESS, ZoraConstants.USDC_DECIMALS,
                               ZoraConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDC'])
        }

        super().__init__(ZoraConstants.NAME, ZoraConstants.NATIVE_TOKEN, ZoraConstants.RPC,
                         ZoraConstants.STARGATE_CHAIN_ID, ZoraConstants.STARGATE_ROUTER_CONTRACT_ADDRESS,
                         ZoraConstants.STARGATE_ROUTER_ETH_CONTRACT_ADDRESS,
                         supported_stablecoins, ZoraConstants.STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS,
                         ZoraConstants.MERKLY_CONTRACT_ADDRESS, ZoraConstants.MERKLY_MAX_TRANSFER,
                         ZoraConstants.MERKLY_NETWORKS)

    def _get_approve_gas_limit(self) -> int:
        return ZoraConstants.APPROVE_GAS_LIMIT
