import base64
import datetime
import hashlib
import hmac
import json
import logging
import time
from decimal import Decimal
from urllib.parse import urlencode

import requests

requests.packages.urllib3.util.connection.HAS_IPV6 = False


class Okx:
    def __init__(self, api_key: str, api_sec: str, api_pass: str, sub_account_name: str = None):
        self.api_key = api_key
        self.api_sec = api_sec
        self.api_pass = api_pass
        self.sub_account_name = sub_account_name
        self.logger = logging

    def __check_transfer_status(self, transfer_id: str, transfer_type: str = None):
        counter = 0
        response = None
        base_url = "https://www.okx.com"
        for _ in range(3):
            while counter < 3:
                tr_type = {
                    "funding": 0,
                    "trading": 0,
                    "funding_sub-trading_main": 2,
                }
                try:
                    params = {
                        "transId": transfer_id,
                        "type": tr_type[transfer_type] if transfer_type is None else 0
                    }
                    sign = self.__generate_sign("GET", "/api/v5/asset/transfer-state?" + urlencode(params))
                    response = requests.get(f"{base_url}/api/v5/asset/transfer-state?" + urlencode(params),
                                            headers=sign)
                    break
                except BaseException:
                    counter += 1
            if response is None:
                raise ConnectionError("Connection error to Okx")
            if response.status_code != 200:
                try:
                    exception_msg = response.json()
                    if exception_msg["code"] == "50102":
                        self.logger.warning("Fail with timestamp. retry in 1 minute")
                        time.sleep(60)
                    else:
                        self.logger.warning("Something went wrong.")
                        return None
                except:
                    raise ConnectionError(response.text)
            else:
                return response.json()["data"][0]["state"]

    def withdraw(self, coin: str, amount: str, address: str,
                 fee_amount: Decimal, chain: str, withdraw_method: int = 4):
        counter = 0
        response = None
        base_url = "https://www.okx.com"
        while counter < 3:
            try:
                params = {
                    "ccy": coin,
                    "amt": amount,
                    "dest": withdraw_method,
                    "toAddr": address,
                    "fee": fee_amount,
                    "chain": chain
                }
                sign = self.__generate_sign("POST", "/api/v5/asset/withdrawal", json.dumps(params))
                response = requests.post(f"{base_url}/api/v5/asset/withdrawal", headers=sign, json=params)
                break
            except BaseException:
                counter += 1
        if response is None:
            raise ConnectionError("Connection error to Okx")
        if response.status_code != 200:
            raise ConnectionError(response.text)
        else:
            try:
                jsobj = response.json()
                if jsobj["code"] != "0":
                    raise ConnectionError(response.text)
                else:
                    self.logger.info(response.text)
            except BaseException:
                raise ConnectionError(response.text)

    def buy_by_market(self, usdt_amount: str | float, ticker: str, stable: str = "USDT") -> dict:
        counter = 0
        response = None
        base_url = "https://www.okx.com"
        self.logger.info("Attempting to buy by market")
        while counter < 3:
            try:
                params = {
                    "instId": f"{ticker}-{stable}",
                    "tdMode": "cash",
                    "side": "buy",
                    "sz": usdt_amount,
                    "tgtCcy": "quote_ccy",
                    "ordType": "market"
                }
                sign = self.__generate_sign("POST", "/api/v5/trade/order", json.dumps(params))
                response = requests.post(f"{base_url}/api/v5/trade/order", headers=sign, json=params)
                break
            except BaseException:
                counter += 1
        if response is None:
            raise ConnectionError("Connection error to Okx")

        if response.status_code != 200:
            raise ConnectionError(response.text)
        else:
            response_json = response.json()
            if response_json["code"] != "0":
                raise ConnectionError(response.text)
            else:
                time.sleep(15)
                return self.get_order_info(response_json["data"][0]["ordId"], ticker, stable)

    def get_order_info(self, order_id: str, ticker: str, stable: str) -> dict:
        counter = 0
        response = None
        base_url = "https://www.okx.com"
        for _ in range(3):
            while counter < 3:
                try:
                    sign = self.__generate_sign("GET", f"/api/v5/trade/order?ordId={order_id}&instId={ticker}-{stable}")
                    response = requests.get(f"{base_url}/api/v5/trade/order?ordId={order_id}&instId={ticker}-{stable}",
                                            headers=sign)
                    break
                except BaseException:
                    counter += 1
            if response is None:
                raise ConnectionError("Connection error to Okx")

            if response.status_code != 200:
                try:
                    exception_msg = response.json()
                    if exception_msg["code"] == "50102":
                        self.logger.warning("Fail with timestamp. retry in 1 minute")
                        time.sleep(60)
                    else:
                        raise BaseException
                except:
                    raise ConnectionError(response.text)
            else:
                response_json = response.json()
                if response_json["code"] != "0":
                    raise ConnectionError(response.text)
                else:
                    fee, quote_amount = self.__get_fee_and_quote_qty(order_id, f"{ticker}-{stable}")
                    return {"amount": Decimal(response_json["data"][0]["accFillSz"]),
                            "quote_amount": quote_amount,
                            "price": Decimal(response_json["data"][0]["avgPx"]),
                            "route": response_json["data"][0]["side"],
                            "instId": response_json["data"][0]["instId"],
                            "fee": fee,
                            "fee_currency": response_json["data"][0]["feeCcy"],
                            "trade_time": response_json["data"][0]["fillTime"]}

    def sell_by_market(self, eth_amount: str, ticker: str, stable: str = "USDT") -> dict:
        counter = 0
        response = None
        base_url = "https://www.okx.com"
        self.logger.info("Attempting to buy by market")
        while counter < 3:
            try:
                params = {
                    "instId": f"{ticker}-{stable}",
                    "tdMode": "cash",
                    "side": "sell",
                    "sz": eth_amount,
                    "tgtCcy": "base_ccy",
                    "ordType": "market"
                }
                sign = self.__generate_sign("POST", "/api/v5/trade/order", json.dumps(params))
                response = requests.post(f"{base_url}/api/v5/trade/order", headers=sign, json=params)
                break
            except BaseException:
                counter += 1
        if response is None:
            raise ConnectionError("Connection error to Okx")
        if response.status_code != 200:
            raise ConnectionError(response.text)
        else:
            response_json = response.json()
            if response_json["code"] != "0":
                raise ConnectionError(response.text)
            else:
                time.sleep(15)
                return self.get_order_info(response_json["data"][0]["ordId"], ticker, stable)

    def get_trade_balance(self, url: str = "/api/v5/account/balance") -> dict:
        counter = 0
        response = None
        base_url = "https://www.okx.com"
        for _ in range(3):
            while counter < 3:
                try:
                    sign = self.__generate_sign("GET", url)
                    response = requests.get(f"{base_url}{url}", headers=sign)
                    break
                except BaseException:
                    counter += 1
            if response is None:
                raise ConnectionError("Connection error to Okx")
            if response.status_code != 200:
                try:
                    exception_msg = response.json()
                    if exception_msg["code"] == "50102":
                        self.logger.warning("Fail with timestamp. retry in 1 minute")
                        time.sleep(60)
                    else:
                        raise BaseException
                except:
                    raise ConnectionError(response.text)
            else:
                response_json = response.json()
                if response_json["code"] != "0":
                    raise ConnectionError(response.text)
                else:
                    balances = {}
                    for balance in response_json['data'][0]["details"]:
                        balances[balance["ccy"]] = Decimal(balance["cashBal"])
                    return balances

    def get_balance(self, url: str = "/api/v5/asset/balances") -> dict:
        counter = 0
        response = None
        base_url = "https://www.okx.com"
        for _ in range(3):
            while counter < 3:
                try:
                    sign = self.__generate_sign("GET", url)
                    response = requests.get(f"{base_url}{url}", headers=sign)
                    break
                except BaseException:
                    counter += 1
            if response is None:
                raise ConnectionError("Connection error to Okx")
            if response.status_code != 200:
                try:
                    exception_msg = response.json()
                    if exception_msg["code"] == "50102":
                        self.logger.warning("Fail with timestamp. retry in 1 minute")
                        time.sleep(60)
                    else:
                        raise BaseException
                except:
                    raise ConnectionError(response.text)
            else:
                response_json = response.json()
                if response_json["code"] != "0":
                    raise ConnectionError(response.text)
                else:
                    balances = {}
                    if len(response_json["data"]) == 0:
                        return balances
                    for balance in response_json['data']:
                        balances[balance["ccy"]] = Decimal(balance["bal"])
                    return balances

    def transfer_between_trading_and_funding_accounts(self, ticker: str, to: str, amount: Decimal,
                                                      from_subaccount: bool = False):
        if to == "funding":
            from_id, to_id = 18, 6
        elif to == "trading" and not from_subaccount:
            from_id, to_id = 6, 18
        elif to == "funding_sub-trading_main" and from_subaccount:
            from_id, to_id = 6, 18
        else:
            return -1

        counter = 0
        response = None
        base_url = "https://www.okx.com"
        self.logger.info("Attempting to transfer to " + to + " account")
        while counter < 3:
            try:
                params = {
                    "ccy": ticker,
                    "amt": str(amount),
                    "from": from_id,
                    "to": to_id,
                    "type": 0 if not from_subaccount else 2
                }
                if from_subaccount:
                    params["subAcct"] = self.sub_account_name
                sign = self.__generate_sign("POST", "/api/v5/asset/transfer", json.dumps(params))
                response = requests.post(f"{base_url}/api/v5/asset/transfer", headers=sign, json=params)
                break
            except BaseException:
                counter += 1
        if response is None:
            raise ConnectionError("Connection error to Okx")
        if response.status_code != 200:
            raise ConnectionError(response.text)
        else:
            response_json = response.json()
            if response_json["code"] != "0":
                raise ConnectionError(response.text)
            else:
                self.logger.info("Checking transfer status...")
                while True:
                    time.sleep(1)
                    transfer_status = self.__check_transfer_status(response_json["data"][0]["transId"], to)
                    self.logger.info(f"Transfer {to} status is {transfer_status}")
                    if transfer_status == "success":
                        break
                    elif transfer_status == "pending":
                        self.logger.info(f"Refetch after 10 seconds")
                        time.sleep(10)
                    else:
                        raise ConnectionError("Transfer failed")

    def get_currencies(self, currency=None) -> dict:
        if currency is None:
            counter = 0
            response = None
            base_url = "https://www.okx.com"
            for _ in range(3):
                while counter < 3:
                    try:
                        print(f"Try #{counter + 1}")
                        sign = self.__generate_sign("GET", "/api/v5/asset/currencies")
                        response = requests.get(f"{base_url}/api/v5/asset/currencies", headers=sign)
                        break
                    except BaseException:
                        counter += 1
                if response is None:
                    raise ConnectionError("Connection error to Okx")
                if response.status_code != 200:
                    try:
                        exception_msg = response.json()
                        if exception_msg["code"] == "50102":
                            self.logger.warning("Fail with timestamp. retry in 1 minute")
                            time.sleep(60)
                        else:
                            raise BaseException
                    except:
                        raise ConnectionError(response.text)
                else:
                    currencies = {}
                    for currency in response.json()["data"]:
                        if currency["ccy"] not in currencies:
                            currencies[currency["ccy"]] = [
                                {"chain": currency["chain"], "minFee": currency["minFee"],
                                 "maxFee": currency["maxFee"]}]
                        else:
                            currencies[currency["ccy"]].append(
                                {"chain": currency["chain"], "minFee": currency["minFee"],
                                 "maxFee": currency["maxFee"]})
                    return currencies

    def __generate_sign(self, method: str, path: str, body: str = "") -> dict:
        ts = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
        if len(ts.split(".")[-1]) > 3:
            ts = ts[:3 - len(ts.split(".")[-1])]
        headers = {
            "OK-ACCESS-KEY": self.api_key,
            "OK-ACCESS-SIGN": "",
            "OK-ACCESS-TIMESTAMP": ts + "Z",
            "OK-ACCESS-PASSPHRASE": self.api_pass
        }
        headers["OK-ACCESS-SIGN"] = base64.b64encode(hmac.new(bytes(self.api_sec, "UTF-8"),
                                                              bytes(
                                                                  headers["OK-ACCESS-TIMESTAMP"] + method + path + body,
                                                                  "UTF-8"),
                                                              hashlib.sha256).digest()).decode("UTF-8")
        return headers

    def __get_fee_and_quote_qty(self, order_id: str, symbol: str) -> tuple[Decimal, Decimal]:
        counter = 0
        response = None
        base_url = "https://www.okx.com"
        for _ in range(3):
            while counter < 3:
                try:
                    params = {
                        "ordId": order_id,
                        "instId": symbol,
                        "instType": "SPOT"
                    }
                    sign = self.__generate_sign("GET", "/api/v5/trade/fills?" + urlencode(params))
                    response = requests.get(f"{base_url}/api/v5/trade/fills?" + urlencode(params),
                                            headers=sign)
                    break
                except BaseException:
                    counter += 1
            if response is None:
                raise ConnectionError("Connection error to Okx")

            if response.status_code != 200:
                raise ConnectionError(response.text)
            else:
                response = response.json()
                fee = Decimal("0")
                quote_qty = Decimal("0")
                for fill in response["data"]:
                    fee += Decimal(fill["fee"])
                    quote_qty += Decimal(fill["fillPx"]) * (Decimal(fill["fillSz"]))
                return fee, quote_qty

    def get_subaccount_balance(self, is_trading: bool) -> dict:
        if not is_trading:
            return self.get_balance(f"/api/v5/asset/subaccount/balances?subAcct={self.sub_account_name}")
        else:
            return self.get_trade_balance(f"/api/v5/account/subaccount/balances?subAcct={self.sub_account_name}")
