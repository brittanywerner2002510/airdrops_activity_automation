class KavaConstants:
    NAME = "Kava"
    NATIVE_TOKEN = "KAVA"
    RPC = "https://kava-evm.publicnode.com"
    CHAIN_ID = 2222
    STARGATE_CHAIN_ID = 177

    USDT_CONTRACT_ADDRESS = "0xAad094F6A75A14417d39f04E690fC216f080A41a"
    USDT_DECIMALS = 6

    STARGATE_ROUTER_CONTRACT_ADDRESS = "0x2F6F07CDcf3588944Bf4C42aC74ff24bF56e7590"
    STARGATE_ROUTER_ETH_CONTRACT_ADDRESS = ""
    STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS = "0x45A01E4e04F14f7A4a6702c74187c5F6222033cd"

    MERKLY_CONTRACT_ADDRESS = "0x04866796aabB6B58e6bC4d91A2aE99105b2C58AE"
    MERKLY_MAX_TRANSFER = "0.98"
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
            "network": "Base",
            "icon": "interface/img/errors.svg"
        },
        {
            "network": "Linea",
            "icon": "interface/img/linea.svg"
        },
        {
            "network": "Metis",
            "icon": "interface/img/metis.svg"
        },
        {
            "network": "Arbitrum",
            "icon": "interface/img/arbitrum-arb-logo.svg"
        }
    ]

    APPROVE_GAS_LIMIT = 1_500_000
