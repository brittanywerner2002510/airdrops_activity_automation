from layerzero.network.network import EVMNetwork
from layerzero.network.arbitrum_nova.constants import ArbitrumNovaConstants
from layerzero.network.stablecoin import Stablecoin
from layerzero.stargate import StargateConstants


class ArbitrumNova(EVMNetwork):

    def __init__(self):
        supported_stablecoins = {
            'USDT': Stablecoin('USDT', ArbitrumNovaConstants.USDT_CONTRACT_ADDRESS, ArbitrumNovaConstants.USDT_DECIMALS,
                               ArbitrumNovaConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDT']),
            'USDC': Stablecoin('USDC', ArbitrumNovaConstants.USDC_CONTRACT_ADDRESS, ArbitrumNovaConstants.USDC_DECIMALS,
                               ArbitrumNovaConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDC'])
        }

        super().__init__(ArbitrumNovaConstants.NAME, ArbitrumNovaConstants.NATIVE_TOKEN, ArbitrumNovaConstants.RPC,
                         ArbitrumNovaConstants.STARGATE_CHAIN_ID, ArbitrumNovaConstants.STARGATE_ROUTER_CONTRACT_ADDRESS,
                         ArbitrumNovaConstants.STARGATE_ROUTER_ETH_CONTRACT_ADDRESS,
                         supported_stablecoins, ArbitrumNovaConstants.STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS,
                         ArbitrumNovaConstants.MERKLY_CONTRACT_ADDRESS, ArbitrumNovaConstants.MERKLY_MAX_TRANSFER,
                         ArbitrumNovaConstants.MERKLY_NETWORKS)

    def _get_approve_gas_limit(self) -> int:
        return ArbitrumNovaConstants.APPROVE_GAS_LIMIT
