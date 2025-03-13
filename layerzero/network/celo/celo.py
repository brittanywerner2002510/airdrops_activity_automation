from layerzero.network.network import EVMNetwork
from layerzero.network.celo.constants import CeloConstants
from layerzero.network.stablecoin import Stablecoin
from layerzero.stargate import StargateConstants


class Celo(EVMNetwork):

    def __init__(self):
        supported_stablecoins = {
            'USDT': Stablecoin('USDT', CeloConstants.USDT_CONTRACT_ADDRESS, CeloConstants.USDT_DECIMALS,
                               CeloConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDT']),
            'USDC': Stablecoin('USDC', CeloConstants.USDC_CONTRACT_ADDRESS, CeloConstants.USDC_DECIMALS,
                               CeloConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDC'])
        }

        super().__init__(CeloConstants.NAME, CeloConstants.NATIVE_TOKEN, CeloConstants.RPC,
                         CeloConstants.STARGATE_CHAIN_ID, CeloConstants.STARGATE_ROUTER_CONTRACT_ADDRESS,
                         CeloConstants.STARGATE_ROUTER_ETH_CONTRACT_ADDRESS,
                         supported_stablecoins, CeloConstants.STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS,
                         CeloConstants.MERKLY_CONTRACT_ADDRESS, CeloConstants.MERKLY_MAX_TRANSFER,
                         CeloConstants.MERKLY_NETWORKS)

    def _get_approve_gas_limit(self) -> int:
        return CeloConstants.APPROVE_GAS_LIMIT
