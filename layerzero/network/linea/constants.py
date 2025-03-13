class LineaConstants:
    NAME = "Linea"
    NATIVE_TOKEN = "ETH"
    RPC = "https://rpc.linea.build"
    EXPLORER = "https://lineascan.build/"
    CHAIN_ID = 59144
    STARGATE_CHAIN_ID = 183

    ETH_CONTRACT_ADDRESS = "0xAad094F6A75A14417d39f04E690fC216f080A41a"
    ETH_DECIMALS = 18

    STARGATE_ROUTER_CONTRACT_ADDRESS = "0x2F6F07CDcf3588944Bf4C42aC74ff24bF56e7590"
    STARGATE_ROUTER_ETH_CONTRACT_ADDRESS = "0x8731d54E9D02c286767d56ac03e8037C07e01e98"
    STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS = "0x45A01E4e04F14f7A4a6702c74187c5F6222033cd"

    MERKLY_CONTRACT_ADDRESS = "0xDB3Bb6D5a8EeEAfc64C66C176900E6B82b23dd5f"
    MERKLY_MAX_TRANSFER = "0.02"
    MERKLY_NETWORKS = [
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
            "network": "Polygon zkEVM",
            "icon": "interface/img/polygon-zkevm.svg"
        },
        {
            "network": "Kava",
            "icon": "interface/img/kava.svg"
        },
        {
            "network": "Base",
            "icon": "interface/img/errors.svg"
        },
        {
            "network": "Mantle",
            "icon": "interface/img/mantle.svg"
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
