from layerzero.network.network import EVMNetwork
from layerzero.network.okex_chain.constants import OkexConstants
from layerzero.network.stablecoin import Stablecoin
from layerzero.stargate import StargateConstants


class Okex(EVMNetwork):

    def __init__(self):
        supported_stablecoins = {
            'USDT': Stablecoin('USDT', OkexConstants.USDT_CONTRACT_ADDRESS, OkexConstants.USDT_DECIMALS,
                               OkexConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDT']),
            'USDC': Stablecoin('USDC', OkexConstants.USDC_CONTRACT_ADDRESS, OkexConstants.USDC_DECIMALS,
                               OkexConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDC'])
        }

        super().__init__(OkexConstants.NAME, OkexConstants.NATIVE_TOKEN, OkexConstants.RPC,
                         OkexConstants.STARGATE_CHAIN_ID, OkexConstants.STARGATE_ROUTER_CONTRACT_ADDRESS,
                         OkexConstants.STARGATE_ROUTER_ETH_CONTRACT_ADDRESS,
                         supported_stablecoins, OkexConstants.STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS,
                         OkexConstants.MERKLY_CONTRACT_ADDRESS, OkexConstants.MERKLY_MAX_TRANSFER,
                         OkexConstants.MERKLY_NETWORKS)

    def _get_approve_gas_limit(self) -> int:
        return OkexConstants.APPROVE_GAS_LIMIT
