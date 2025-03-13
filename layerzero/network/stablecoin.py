from dataclasses import dataclass


@dataclass
class Stablecoin:
    coin: str
    contract_address: str
    decimals: int
    stargate_chain_id: int
    stargate_pool_id: int
