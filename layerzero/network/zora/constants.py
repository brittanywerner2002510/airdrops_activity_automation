class ZoraConstants:
    NAME = "Zora"
    NATIVE_TOKEN = "ETH"
    RPC = "https://rpc.zora.energy"
    EXPLORER = "https://explorer.zora.energy/"
    CHAIN_ID = 7777777
    STARGATE_CHAIN_ID = 195

    USDC_CONTRACT_ADDRESS = "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8"
    USDC_DECIMALS = 6

    USDT_CONTRACT_ADDRESS = "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9"
    USDT_DECIMALS = 6

    STARGATE_ROUTER_CONTRACT_ADDRESS = "0x53Bf833A5d6c4ddA888F69c22C88C9f356a41614"
    STARGATE_ROUTER_ETH_CONTRACT_ADDRESS = ""
    STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS = "0x1cF31666c06ac3401ed0C1c6346C4A9425dd7De4"

    MERKLY_CONTRACT_ADDRESS = "0xFFd57B46BD670B0461c7C3EBBaEDC4CdB7c4FB80"
    MERKLY_MAX_TRANSFER = "0.02"
    MERKLY_NETWORKS = [
        {
            "network": "Optimism",
            "icon": "interface/img/optimism.svg"
        },
        {
            "network": "Polygon",
            "icon": "interface/img/polygon.svg"
        },
        {
            "network": "Arbitrum",
            "icon": "interface/img/arbitrum-arb-logo.svg"
        },
        {
            "network": "Base",
            "icon": "interface/img/errors.svg"
        }
    ]

    APPROVE_GAS_LIMIT = 100_000
