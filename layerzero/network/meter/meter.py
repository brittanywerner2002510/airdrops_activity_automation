from layerzero.network.network import EVMNetwork
from layerzero.network.meter.constants import MeterConstants
from layerzero.network.stablecoin import Stablecoin
from layerzero.stargate import StargateConstants


class Meter(EVMNetwork):

    def __init__(self):
        supported_stablecoins = {
            'USDT': Stablecoin('USDT', MeterConstants.USDT_CONTRACT_ADDRESS, MeterConstants.USDT_DECIMALS,
                               MeterConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDT']),
            'USDC': Stablecoin('USDC', MeterConstants.USDC_CONTRACT_ADDRESS, MeterConstants.USDC_DECIMALS,
                               MeterConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDC'])
        }

        super().__init__(MeterConstants.NAME, MeterConstants.NATIVE_TOKEN, MeterConstants.RPC,
                         MeterConstants.STARGATE_CHAIN_ID, MeterConstants.STARGATE_ROUTER_CONTRACT_ADDRESS,
                         MeterConstants.STARGATE_ROUTER_ETH_CONTRACT_ADDRESS,
                         supported_stablecoins, MeterConstants.STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS,
                         MeterConstants.MERKLY_CONTRACT_ADDRESS, MeterConstants.MERKLY_MAX_TRANSFER,
                         MeterConstants.MERKLY_NETWORKS)

    def _get_approve_gas_limit(self) -> int:
        return MeterConstants.APPROVE_GAS_LIMIT
