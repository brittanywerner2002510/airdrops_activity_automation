class CoredaoConstants:
    NAME = "CORE"
    NATIVE_TOKEN = "CORE"
    RPC = "https://rpc.coredao.org"
    CHAIN_ID = 1116
    STARGATE_CHAIN_ID = 153

    USDT_CONTRACT_ADDRESS = "0x900101d06a7426441ae63e9ab3b9b0f63be145f1"
    USDT_DECIMALS = 6

    STARGATE_ROUTER_CONTRACT_ADDRESS = "0x4a364f8c717cAAD9A442737Eb7b8A55cc6cf18D8"
    STARGATE_ROUTER_ETH_CONTRACT_ADDRESS = ""
    STARGATE_FEE_LIBRARY_CONTRACT_ADDRESS = "0xCA6522116e8611A346D53Cc2005AC4192e3fc2BC"

    MERKLY_CONTRACT_ADDRESS = "0xCA230856343C300f0cc2Bd77C89F0fCBeDc45B0f"
    MERKLY_MAX_TRANSFER = "0.25"
    MERKLY_NETWORKS = [
        {
            "network": "Polygon",
            "icon": "interface/img/polygon.svg"
        },
        {
            "network": "BSC",
            "icon": "interface/img/bsc.svg"
        }
    ]

    APPROVE_GAS_LIMIT = 100_000
