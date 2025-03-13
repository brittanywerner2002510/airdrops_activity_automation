from layerzero.network.network import EVMNetwork
from layerzero.network.zksync_era.constants import ZkSyncEraConstants
from layerzero.network.stablecoin import Stablecoin
from layerzero.stargate import StargateConstants


class ZkSyncEra(EVMNetwork):

    def __init__(self):
        supported_stablecoins = {
            'USDT': Stablecoin('USDT', ZkSyncEraConstants.USDT_CONTRACT_ADDRESS, ZkSyncEraConstants.USDT_DECIMALS,
                               ZkSyncEraConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDT']),
            'USDC': Stablecoin('USDC', ZkSyncEraConstants.USDC_CONTRACT_ADDRESS, ZkSyncEraConstants.USDC_DECIMALS,
                               ZkSyncEraConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDC'])
        }

        super().__init__(ZkSyncEraConstants.NAME, ZkSyncEraConstants.NATIVE_TOKEN, ZkSyncEraConstants.RPC,
                         ZkSyncEraConstants.STARGATE_CHAIN_ID, ZkSyncEraConstants.STARGATE_ROUTER_CONTRACT_ADDRESS,
                         ZkSyncEraConstants.STARGATE_ROUTER_ETH_CONTRACT_ADDRESS,
                         supported_stablecoins, ZkSyncEraConstants.STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS,
                         ZkSyncEraConstants.MERKLY_CONTRACT_ADDRESS, ZkSyncEraConstants.MERKLY_MAX_TRANSFER,
                         ZkSyncEraConstants.MERKLY_NETWORKS)

    def _get_approve_gas_limit(self) -> int:
        return ZkSyncEraConstants.APPROVE_GAS_LIMIT
