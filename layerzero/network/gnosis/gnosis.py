from layerzero.network.network import EVMNetwork
from layerzero.network.gnosis.constants import GnosisConstants
from layerzero.network.stablecoin import Stablecoin
from layerzero.stargate import StargateConstants


class Gnosis(EVMNetwork):

    def __init__(self):
        supported_stablecoins = {
            'USDT': Stablecoin('USDT', GnosisConstants.USDT_CONTRACT_ADDRESS, GnosisConstants.USDT_DECIMALS,
                               GnosisConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDT']),
            'USDC': Stablecoin('USDC', GnosisConstants.USDC_CONTRACT_ADDRESS, GnosisConstants.USDC_DECIMALS,
                               GnosisConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDC'])
        }

        super().__init__(GnosisConstants.NAME, GnosisConstants.NATIVE_TOKEN, GnosisConstants.RPC,
                         GnosisConstants.STARGATE_CHAIN_ID, GnosisConstants.STARGATE_ROUTER_CONTRACT_ADDRESS,
                         GnosisConstants.STARGATE_ROUTER_ETH_CONTRACT_ADDRESS,
                         supported_stablecoins, GnosisConstants.STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS,
                         GnosisConstants.MERKLY_CONTRACT_ADDRESS, GnosisConstants.MERKLY_MAX_TRANSFER,
                         GnosisConstants.MERKLY_NETWORKS)

    def _get_approve_gas_limit(self) -> int:
        return GnosisConstants.APPROVE_GAS_LIMIT
