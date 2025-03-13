class GnosisConstants:
    NAME = "Gnosis"
    NATIVE_TOKEN = "XDAI"
    RPC = "https://rpc.ankr.com/gnosis"
    CHAIN_ID = 100
    STARGATE_CHAIN_ID = 145

    USDC_CONTRACT_ADDRESS = "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8"
    USDC_DECIMALS = 6

    USDT_CONTRACT_ADDRESS = "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9"
    USDT_DECIMALS = 6

    STARGATE_ROUTER_CONTRACT_ADDRESS = "0x53Bf833A5d6c4ddA888F69c22C88C9f356a41614"
    STARGATE_ROUTER_ETH_CONTRACT_ADDRESS = ""
    STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS = "0x1cF31666c06ac3401ed0C1c6346C4A9425dd7De4"

    MERKLY_CONTRACT_ADDRESS = "0xb58f5110855fbef7a715d325d60543e7d4c18143"
    MERKLY_MAX_TRANSFER = "0.05"
    MERKLY_NETWORKS = [
        {
            "network": "Optimism",
            "icon": "interface/img/optimism.svg"
        },
        {
            "network": "Avalanche",
            "icon": "interface/img/avalanche.svg"
        },
        {
            "network": "Fantom",
            "icon": "interface/img/fantom.svg"
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
            "network": "Celo",
            "icon": "interface/img/celo.svg"
        },
        {
            "network": "Klaytn",
            "icon": "interface/img/klaytn.svg"
        },
        {
            "network": "Metis",
            "icon": "interface/img/metis.svg"
        },
        {
            "network": "Fuse",
            "icon": "interface/img/fuse.svg"
        },
        {
            "network": "Arbitrum",
            "icon": "interface/img/arbitrum-arb-logo.svg"
        }
    ]

    APPROVE_GAS_LIMIT = 1_500_000
