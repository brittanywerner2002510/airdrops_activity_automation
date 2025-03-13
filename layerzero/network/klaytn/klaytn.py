from layerzero.network.network import EVMNetwork
from layerzero.network.klaytn.constants import KlaytnConstants
from layerzero.network.stablecoin import Stablecoin
from layerzero.stargate import StargateConstants


class Klaytn(EVMNetwork):

    def __init__(self):
        supported_stablecoins = {
            'USDT': Stablecoin('USDT', KlaytnConstants.USDT_CONTRACT_ADDRESS, KlaytnConstants.USDT_DECIMALS,
                               KlaytnConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDT']),
            'USDC': Stablecoin('USDC', KlaytnConstants.USDC_CONTRACT_ADDRESS, KlaytnConstants.USDC_DECIMALS,
                               KlaytnConstants.STARGATE_CHAIN_ID, StargateConstants.POOLS['USDC'])
        }

        super().__init__(KlaytnConstants.NAME, KlaytnConstants.NATIVE_TOKEN, KlaytnConstants.RPC,
                         KlaytnConstants.STARGATE_CHAIN_ID, KlaytnConstants.STARGATE_ROUTER_CONTRACT_ADDRESS,
                         KlaytnConstants.STARGATE_ROUTER_ETH_CONTRACT_ADDRESS,
                         supported_stablecoins, KlaytnConstants.STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS,
                         KlaytnConstants.MERKLY_CONTRACT_ADDRESS, KlaytnConstants.MERKLY_MAX_TRANSFER,
                         KlaytnConstants.MERKLY_NETWORKS)

    def _get_approve_gas_limit(self) -> int:
        return KlaytnConstants.APPROVE_GAS_LIMIT
