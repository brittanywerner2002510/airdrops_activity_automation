from layerzero.network.network import EVMNetwork
from layerzero.network.mantle.constants import MantleConstants
from layerzero.network.stablecoin import Stablecoin
from layerzero.stargate import StargateConstants


class Mantle(EVMNetwork):

    def __init__(self):
        supported_stablecoins = {
            'USDT': Stablecoin('USDT', MantleConstants.USDT_CONTRACT_ADDRESS, MantleConstants.USDT_DECIMALS,
                               MantleConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDT']),
            'USDC': Stablecoin('USDC', MantleConstants.USDC_CONTRACT_ADDRESS, MantleConstants.USDC_DECIMALS,
                               MantleConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDC'])
        }

        super().__init__(MantleConstants.NAME, MantleConstants.NATIVE_TOKEN, MantleConstants.RPC,
                         MantleConstants.STARGATE_CHAIN_ID, MantleConstants.STARGATE_ROUTER_CONTRACT_ADDRESS,
                         MantleConstants.STARGATE_ROUTER_ETH_CONTRACT_ADDRESS,
                         supported_stablecoins, MantleConstants.STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS,
                         MantleConstants.MERKLY_CONTRACT_ADDRESS, MantleConstants.MERKLY_MAX_TRANSFER,
                         MantleConstants.MERKLY_NETWORKS)

    def _get_approve_gas_limit(self) -> int:
        return MantleConstants.APPROVE_GAS_LIMIT
