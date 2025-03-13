from layerzero.network.network import EVMNetwork
from layerzero.network.fuse.constants import FuseConstants
from layerzero.network.stablecoin import Stablecoin
from layerzero.stargate import StargateConstants


class Fuse(EVMNetwork):

    def __init__(self):
        supported_stablecoins = {
            'USDT': Stablecoin('USDT', FuseConstants.USDT_CONTRACT_ADDRESS, FuseConstants.USDT_DECIMALS,
                               FuseConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDT']),
            'USDC': Stablecoin('USDC', FuseConstants.USDC_CONTRACT_ADDRESS, FuseConstants.USDC_DECIMALS,
                               FuseConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDC'])
        }

        super().__init__(FuseConstants.NAME, FuseConstants.NATIVE_TOKEN, FuseConstants.RPC,
                         FuseConstants.STARGATE_CHAIN_ID, FuseConstants.STARGATE_ROUTER_CONTRACT_ADDRESS,
                         FuseConstants.STARGATE_ROUTER_ETH_CONTRACT_ADDRESS,
                         supported_stablecoins, FuseConstants.STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS,
                         FuseConstants.MERKLY_CONTRACT_ADDRESS, FuseConstants.MERKLY_MAX_TRANSFER,
                         FuseConstants.MERKLY_NETWORKS)

    def _get_approve_gas_limit(self) -> int:
        return FuseConstants.APPROVE_GAS_LIMIT
