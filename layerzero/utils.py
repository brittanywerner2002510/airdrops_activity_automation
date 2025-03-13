from layerzero.network import *
from eth_account import Account

NETWORKS = {
    "Arbitrum": Arbitrum(),
    "Avalanche": Avalanche(),
    "BSC": BSC(),
    "Ethereum": Ethereum(),
    "Fantom": Fantom(),
    "Optimism": Optimism(),
    "Polygon": Polygon(),
    "Coredao": Coredao(),
    "Base": Base(),
    "Arbitrum Nova": ArbitrumNova(),
    "Canto": Canto(),
    "Celo": Celo(),
    "DFK": Dfk(),
    "Fuse": Fuse(),
    "Gnosis": Gnosis(),
    "Harmony One": Harmony(),
    "Kava": Kava(),
    "Linea": Linea(),
    "Mantle": Mantle(),
    "Meter": Meter(),
    "Metis": Metis(),
    "Moonbeam": Moonbeam(),
    "Moonriver": Moonriver(),
    "OKEX chain": Okex(),
    "Polygon zkEVM": PolygonZk(),
    "Sepolia": Sepolia(),
    "Tenet": Tenet(),
    "zkSync Era": ZkSyncEra(),
    "Zora": Zora()
}


def get_networks_objects(networks: list[str]) -> list[EVMNetwork]:
    objects_list = []
    for network in networks:
        network_object = NETWORKS[network]
        objects_list.append(network_object)
    return objects_list


def get_address_from_private_key(private_key):
    account = Account.from_key(private_key)
    return account.address
