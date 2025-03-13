from layerzero.network.network import EVMNetwork
from layerzero.network.dfk.constants import DfkConstants
from layerzero.network.stablecoin import Stablecoin
from layerzero.stargate import StargateConstants


class Dfk(EVMNetwork):

    def __init__(self):
        supported_stablecoins = {
            'USDT': Stablecoin('USDT', DfkConstants.USDT_CONTRACT_ADDRESS, DfkConstants.USDT_DECIMALS,
                               DfkConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDT']),
            'USDC': Stablecoin('USDC', DfkConstants.USDC_CONTRACT_ADDRESS, DfkConstants.USDC_DECIMALS,
                               DfkConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDC'])
        }

        super().__init__(DfkConstants.NAME, DfkConstants.NATIVE_TOKEN, DfkConstants.RPC,
                         DfkConstants.STARGATE_CHAIN_ID, DfkConstants.STARGATE_ROUTER_CONTRACT_ADDRESS,
                         DfkConstants.STARGATE_ROUTER_ETH_CONTRACT_ADDRESS,
                         supported_stablecoins, DfkConstants.STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS,
                         DfkConstants.MERKLY_CONTRACT_ADDRESS, DfkConstants.MERKLY_MAX_TRANSFER,
                         DfkConstants.MERKLY_NETWORKS)

    def _get_approve_gas_limit(self) -> int:
        return DfkConstants.APPROVE_GAS_LIMIT
