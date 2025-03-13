class OkexConstants:
    NAME = "OKEx Chain"
    NATIVE_TOKEN = "OKT"
    RPC = "https://exchainrpc.okex.org"
    EXPLORER = "https://www.oklink.com/ru"
    CHAIN_ID = 66
    STARGATE_CHAIN_ID = 155

    USDC_CONTRACT_ADDRESS = "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8"
    USDC_DECIMALS = 6

    USDT_CONTRACT_ADDRESS = "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9"
    USDT_DECIMALS = 6

    STARGATE_ROUTER_CONTRACT_ADDRESS = "0x53Bf833A5d6c4ddA888F69c22C88C9f356a41614"
    STARGATE_ROUTER_ETH_CONTRACT_ADDRESS = ""
    STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS = "0x1cF31666c06ac3401ed0C1c6346C4A9425dd7De4"

    MERKLY_CONTRACT_ADDRESS = "0xa0a54dADc2a1F198C58Fd0739BA7dF40Ffd366Dc"
    MERKLY_MAX_TRANSFER = "0.25"
    MERKLY_NETWORKS = [
        {
            "network": "Avalanche",
            "icon": "interface/img/avalanche.svg"
        },
        {
            "network": "Polygon",
            "icon": "interface/img/polygon.svg"
        },
        {
            "network": "BSC",
            "icon": "interface/img/bsc.svg"
        },
        {
            "network": "Arbitrum",
            "icon": "interface/img/arbitrum-arb-logo.svg"
        }
    ]

    APPROVE_GAS_LIMIT = 1_500_000
