from layerzero.network.network import EVMNetwork
from layerzero.network.bsc.constants import BSCConstants
from layerzero.network.stablecoin import Stablecoin
from layerzero.stargate import StargateConstants


class BSC(EVMNetwork):

    def __init__(self):
        supported_stablecoins = {
            'USDT': Stablecoin('USDT', BSCConstants.USDT_CONTRACT_ADDRESS, BSCConstants.USDT_DECIMALS,
                               BSCConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDT']),
            'BUSD': Stablecoin('BUSD', BSCConstants.BUSD_CONTRACT_ADDRESS, BSCConstants.BUSD_DECIMALS,
                               BSCConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['BUSD'])
        }

        super().__init__(BSCConstants.NAME, BSCConstants.NATIVE_TOKEN, BSCConstants.RPC,
                         BSCConstants.STARGATE_CHAIN_ID, BSCConstants.STARGATE_ROUTER_CONTRACT_ADDRESS,
                         BSCConstants.STARGATE_ROUTER_ETH_CONTRACT_ADDRESS,
                         supported_stablecoins, BSCConstants.STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS,
                         BSCConstants.MERKLY_CONTRACT_ADDRESS, BSCConstants.MERKLY_MAX_TRANSFER,
                         BSCConstants.MERKLY_NETWORKS)

    def _get_approve_gas_limit(self) -> int:
        return BSCConstants.APPROVE_GAS_LIMIT
