class BaseConstants:
    NAME = "Base"
    NATIVE_TOKEN = "ETH"
    RPC = "https://base.blockpi.network/v1/rpc/public"
    EXPLORER = "https://base.blockscout.com/"
    CHAIN_ID = 8453
    STARGATE_CHAIN_ID = 184

    USDC_CONTRACT_ADDRESS = "0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA"
    USDC_DECIMALS = 6

    ETH_CONTRACT_ADDRESS = "0x28fc411f9e1c480AD312b3d9C60c22b965015c6B"
    ETH_DECIMALS = 18

    STARGATE_ROUTER_CONTRACT_ADDRESS = "0x45f1A95A4D3f3836523F5c83673c797f4d4d263B"
    STARGATE_ROUTER_ETH_CONTRACT_ADDRESS = "0x50B6EbC2103BFEc165949CC946d739d5650d7ae4"
    STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS = "0x9d1B1669c73b033DFe47ae5a0164Ab96df25B944"

    MERKLY_CONTRACT_ADDRESS = "0xF882c982a95F4D3e8187eFE12713835406d11840"
    MERKLY_MAX_TRANSFER = "0.02"
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
            "network": "Polygon zkEVM",
            "icon": "interface/img/polygon-zkevm.svg"
        },
        {
            "network": "Kava",
            "icon": "interface/img/kava.svg"
        },
        {
            "network": "Linea",
            "icon": "interface/img/linea.svg"
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
