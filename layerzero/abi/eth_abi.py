STARGATE_ETH_ABI = [
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_stargateEthVault",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "_stargateRouter",
                "type": "address"
            },
            {
                "internalType": "uint16",
                "name": "_poolId",
                "type": "uint16"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "inputs": [

        ],
        "name": "addLiquidityETH",
        "outputs": [

        ],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [

        ],
        "name": "poolId",
        "outputs": [
            {
                "internalType": "uint16",
                "name": "",
                "type": "uint16"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [

        ],
        "name": "stargateEthVault",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [

        ],
        "name": "stargateRouter",
        "outputs": [
            {
                "internalType": "contract IStargateRouter",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint16",
                "name": "_dstChainId",
                "type": "uint16"
            },
            {
                "internalType": "address payable",
                "name": "_refundAddress",
                "type": "address"
            },
            {
                "internalType": "bytes",
                "name": "_toAddress",
                "type": "bytes"
            },
            {
                "internalType": "uint256",
                "name": "_amountLD",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "_minAmountLD",
                "type": "uint256"
            }
        ],
        "name": "swapETH",
        "outputs": [

        ],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "stateMutability": "payable",
        "type": "receive"
    }
]
