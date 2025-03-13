import requests
from aptos_sdk.client import RestClient, ClientConfig
from aptos_sdk.metadata import Metadata
from fake_useragent import UserAgent


class RestClientWithProxy(RestClient):
    def __init__(self, base_url: str, client_config: ClientConfig = ClientConfig(), proxy: dict = None,
                 user_agent: str = None, client_id: str = "aptos-ts-sdk/1.13.3", logger=None):
        self.logger = logger
        self.logger.warning("This proxy client is HACK for aptos-sdk which doesnt support proxies."
                            "This hack can be broken after aptos-sdk update!")
        self.logger.warning(f"I will use header `X-Aptos-Client: {client_id}` which may be outdated")
        self.base_url = base_url
        self.client = requests.Session()
        if proxy is not None:
            self.client.proxies.update(proxy)
        headers = {
            Metadata.APTOS_HEADER: client_id,
        }
        if user_agent is not None:
            headers["User-Agent"] = user_agent
            self.user_agent = user_agent
        else:
            ua = UserAgent(os="windows", browsers=["chrome"])
            headers["User-Agent"] = ua.random
            self.user_agent = headers["User-Agent"]
        self.client.headers.update(
            headers
        )
        self.client_config = client_config
        self.chain_id = int(self.info()["chain_id"])
