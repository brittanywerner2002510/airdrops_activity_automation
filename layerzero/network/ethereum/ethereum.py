from layerzero.network.network import EVMNetwork
from layerzero.network.ethereum.constants import EthereumConstants
from layerzero.network.stablecoin import Stablecoin
from layerzero.stargate import StargateConstants


class Ethereum(EVMNetwork):

    def __init__(self):
        supported_stablecoins = {
            'USDT': Stablecoin('USDT', EthereumConstants.USDT_CONTRACT_ADDRESS, EthereumConstants.USDT_DECIMALS,
                               EthereumConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDT']),
            'USDC': Stablecoin('USDC', EthereumConstants.USDC_CONTRACT_ADDRESS, EthereumConstants.USDC_DECIMALS,
                               EthereumConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDC']),
            'ETH': Stablecoin('ETH', EthereumConstants.ETH_CONTRACT_ADDRESS, EthereumConstants.ETH_DECIMALS,
                              EthereumConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['ETH'])
        }

        super().__init__(EthereumConstants.NAME, EthereumConstants.NATIVE_TOKEN, EthereumConstants.RPC,
                         EthereumConstants.STARGATE_CHAIN_ID, EthereumConstants.STARGATE_ROUTER_CONTRACT_ADDRESS,
                         EthereumConstants.STARGATE_ROUTER_ETH_CONTRACT_ADDRESS,
                         supported_stablecoins, EthereumConstants.STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS,
                         EthereumConstants.MERKLY_CONTRACT_ADDRESS, EthereumConstants.MERKLY_MAX_TRANSFER,
                         EthereumConstants.MERKLY_NETWORKS)

    def _get_approve_gas_limit(self) -> int:
        return EthereumConstants.APPROVE_GAS_LIMIT
