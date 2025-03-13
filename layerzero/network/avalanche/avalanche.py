from layerzero.network.network import EVMNetwork
from layerzero.network.avalanche.constants import AvalancheConstants
from layerzero.network.stablecoin import Stablecoin
from layerzero.stargate import StargateConstants


class Avalanche(EVMNetwork):

    def __init__(self):
        supported_stablecoins = {
            'USDT': Stablecoin('USDT', AvalancheConstants.USDT_CONTRACT_ADDRESS, AvalancheConstants.USDT_DECIMALS,
                               AvalancheConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDT']),
            'USDC': Stablecoin('USDC', AvalancheConstants.USDC_CONTRACT_ADDRESS, AvalancheConstants.USDC_DECIMALS,
                               AvalancheConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDC'])
        }

        super().__init__(AvalancheConstants.NAME, AvalancheConstants.NATIVE_TOKEN, AvalancheConstants.RPC,
                         AvalancheConstants.STARGATE_CHAIN_ID, AvalancheConstants.STARGATE_ROUTER_CONTRACT_ADDRESS,
                         AvalancheConstants.STARGATE_ROUTER_ETH_CONTRACT_ADDRESS,
                         supported_stablecoins, AvalancheConstants.STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS,
                         AvalancheConstants.MERKLY_CONTRACT_ADDRESS, AvalancheConstants.MERKLY_MAX_TRANSFER,
                         AvalancheConstants.MERKLY_NETWORKS)

    def _get_approve_gas_limit(self) -> int:
        return AvalancheConstants.APPROVE_GAS_LIMIT
