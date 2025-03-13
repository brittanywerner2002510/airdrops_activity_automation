import time

from eth_abi import encode
from web3 import Web3

from layerzero.abi import ABI_MERKLY_REFUEL
from layerzero.network.network import EVMNetwork


def get_adapter_params(gas_limit: int, amount: int):
    return Web3.to_hex(encode(["uint16", "uint64", "uint256"], [2, gas_limit, amount])[30:])


def int_to_decimal(qty: int, decimal: int) -> int:
    return int(qty * int("".join(["1"] + ["0"] * decimal)))


def check_merkly_fees(src_network: EVMNetwork, dst_network: EVMNetwork, key: str) -> dict:
    w3 = Web3(Web3.HTTPProvider(src_network.rpc))
    address = w3.eth.account.from_key(key).address
    contract = w3.eth.contract(address=Web3.to_checksum_address(src_network.merkly_address), abi=ABI_MERKLY_REFUEL)
    adapter_params = get_adapter_params(250000, 1) + address[2:].lower()
    try:
        send_value = contract.functions.estimateGasBridgeFee(dst_network.stargate_chain_id,
                                                             False, adapter_params).call()
        refuel_cost = w3.from_wei(send_value[0], "ether")
        return {"code": 1, "msg": f"Refuel cost: {format(refuel_cost, '.5f')} "
                                  f"{src_network.native_token.upper()}", "data": send_value[0]}
    except Exception as error:
        return {"code": -1, "msg": error}


def merkly_refuel(private_key: str, src_network: EVMNetwork, dst_network: EVMNetwork, native_amount: int) -> dict:
    max_time_check_tx_status = 100
    try:
        w3 = Web3(Web3.HTTPProvider(src_network.rpc))
        account = w3.eth.account.from_key(private_key)
        address = account.address
        contract = w3.eth.contract(address=Web3.to_checksum_address(src_network.merkly_address),
                                   abi=ABI_MERKLY_REFUEL)
        value = int_to_decimal(native_amount, 18)
        adapter_params = get_adapter_params(250000, value) + address[2:].lower()
        send_value = contract.functions.estimateGasBridgeFee(dst_network.stargate_chain_id,
                                                             False, adapter_params).call()
        contract_txn = contract.functions.bridgeGas(
            dst_network.stargate_chain_id,
            '0x0000000000000000000000000000000000000000',
            adapter_params
        ).build_transaction(
            {
                "from": address,
                "value": send_value[0],
                "nonce": w3.eth.get_transaction_count(address),
                'gasPrice': 0,
                'gas': 0,
            }
        )
        if src_network.name == 'BSC':
            contract_txn['gasPrice'] = 1000000000
        else:
            contract_txn['gasPrice'] = w3.eth.gas_price

        contract_txn['gas'] = w3.eth.estimate_gas(contract_txn)
        signed_tx = w3.eth.account.sign_transaction(contract_txn, private_key)
        raw_tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_hash = w3.to_hex(raw_tx_hash)
        start_time_stamp = int(time.time())
        while True:
            try:
                status_ = w3.eth.get_transaction_receipt(tx_hash)
                status = status_["status"]
                if status in [0, 1]:
                    return {"code": 1, "msg": status, "data": tx_hash}
            except Exception as error:
                time_stamp = int(time.time())
                if time_stamp - start_time_stamp > max_time_check_tx_status:
                    return {"code": -1, "msg": error}
                time.sleep(3)
    except Exception as error:
        return {"code": -1, "msg": error}
