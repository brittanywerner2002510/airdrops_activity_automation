from layerzero.network.network import EVMNetwork
from layerzero.network.sepolia.constants import SepoliaConstants
from layerzero.network.stablecoin import Stablecoin
from layerzero.stargate import StargateConstants


class Sepolia(EVMNetwork):

    def __init__(self):
        supported_stablecoins = {
            'USDT': Stablecoin('USDT', SepoliaConstants.USDT_CONTRACT_ADDRESS, SepoliaConstants.USDT_DECIMALS,
                               SepoliaConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDT']),
            'USDC': Stablecoin('USDC', SepoliaConstants.USDC_CONTRACT_ADDRESS, SepoliaConstants.USDC_DECIMALS,
                               SepoliaConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDC'])
        }

        super().__init__(SepoliaConstants.NAME, SepoliaConstants.NATIVE_TOKEN, SepoliaConstants.RPC,
                         SepoliaConstants.STARGATE_CHAIN_ID, SepoliaConstants.STARGATE_ROUTER_CONTRACT_ADDRESS,
                         SepoliaConstants.STARGATE_ROUTER_ETH_CONTRACT_ADDRESS,
                         supported_stablecoins, SepoliaConstants.STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS,
                         SepoliaConstants.MERKLY_CONTRACT_ADDRESS, SepoliaConstants.MERKLY_MAX_TRANSFER,
                         SepoliaConstants.MERKLY_NETWORKS)

    def _get_approve_gas_limit(self) -> int:
        return SepoliaConstants.APPROVE_GAS_LIMIT
