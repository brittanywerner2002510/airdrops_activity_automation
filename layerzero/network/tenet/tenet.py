from layerzero.network.network import EVMNetwork
from layerzero.network.tenet.constants import TenetConstants
from layerzero.network.stablecoin import Stablecoin
from layerzero.stargate import StargateConstants


class Tenet(EVMNetwork):

    def __init__(self):
        supported_stablecoins = {
            'USDT': Stablecoin('USDT', TenetConstants.USDT_CONTRACT_ADDRESS, TenetConstants.USDT_DECIMALS,
                               TenetConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDT']),
            'USDC': Stablecoin('USDC', TenetConstants.USDC_CONTRACT_ADDRESS, TenetConstants.USDC_DECIMALS,
                               TenetConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDC'])
        }

        super().__init__(TenetConstants.NAME, TenetConstants.NATIVE_TOKEN, TenetConstants.RPC,
                         TenetConstants.STARGATE_CHAIN_ID, TenetConstants.STARGATE_ROUTER_CONTRACT_ADDRESS,
                         TenetConstants.STARGATE_ROUTER_ETH_CONTRACT_ADDRESS,
                         supported_stablecoins, TenetConstants.STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS,
                         TenetConstants.MERKLY_CONTRACT_ADDRESS, TenetConstants.MERKLY_MAX_TRANSFER,
                         TenetConstants.MERKLY_NETWORKS)

    def _get_approve_gas_limit(self) -> int:
        return TenetConstants.APPROVE_GAS_LIMIT
