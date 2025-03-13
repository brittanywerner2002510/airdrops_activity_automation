from layerzero.network.network import EVMNetwork
from layerzero.network.arbitrum.constants import ArbitrumConstants
from layerzero.network.stablecoin import Stablecoin
from layerzero.stargate import StargateConstants


class Arbitrum(EVMNetwork):

    def __init__(self):
        supported_stablecoins = {
            'USDT': Stablecoin('USDT', ArbitrumConstants.USDT_CONTRACT_ADDRESS, ArbitrumConstants.USDT_DECIMALS,
                               ArbitrumConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDT']),
            'USDC': Stablecoin('USDC', ArbitrumConstants.USDC_CONTRACT_ADDRESS, ArbitrumConstants.USDC_DECIMALS,
                               ArbitrumConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDC']),
            'ETH': Stablecoin('ETH', ArbitrumConstants.ETH_CONTRACT_ADDRESS, ArbitrumConstants.ETH_DECIMALS,
                              ArbitrumConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['ETH'])
        }

        super().__init__(ArbitrumConstants.NAME, ArbitrumConstants.NATIVE_TOKEN, ArbitrumConstants.RPC,
                         ArbitrumConstants.STARGATE_CHAIN_ID, ArbitrumConstants.STARGATE_ROUTER_CONTRACT_ADDRESS,
                         ArbitrumConstants.STARGATE_ROUTER_ETH_CONTRACT_ADDRESS, supported_stablecoins,
                         ArbitrumConstants.STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS,
                         ArbitrumConstants.MERKLY_CONTRACT_ADDRESS, ArbitrumConstants.MERKLY_MAX_TRANSFER,
                         ArbitrumConstants.MERKLY_NETWORKS)

    def _get_approve_gas_limit(self) -> int:
        return ArbitrumConstants.APPROVE_GAS_LIMIT
