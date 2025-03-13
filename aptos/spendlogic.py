import datetime
import random
import time
from decimal import Decimal

import requests
from requests.exceptions import SSLError

from aptos.RestClientWithProxy import RestClientWithProxy
from aptos.cex.okx import Okx
from aptos.constants import TIMING
from aptos.lending.abel_finance.abel_finance import AbelFinance
from aptos.lending.aptin.aptin import Aptin
from aptos.lending.aries.aries import Aries
from aptos.liquidswap.liquidswap import LiquidSwap
from aptos.pancakeswap.pancakeswap import PancakeSwap
from aptos.token_addresses import TOKENS
from aptos.wallet import Wallet


class Spendlogic:
    def __init__(self, init_headers: dict):
        self.logger = init_headers["logger"]
        self.eth_acc = init_headers["pk"]
        self.okx_account = Okx(**init_headers["okx_creds"])
        self.okx_account.logger = init_headers["logger"]
        self.proxy = self.__setup_proxy(init_headers["proxy"])
        self.event = init_headers["event"]
        self.user_agent = RestClientWithProxy("https://rpc.ankr.com/http/aptos/v1",
                                              proxy={'http': self.proxy, 'https': self.proxy},
                                              logger=self.logger).user_agent
        self.wallet_apt = Wallet(self.eth_acc, proxy=self.proxy, user_agent=self.user_agent, logger=self.logger)
        self.slippage = Decimal(str(init_headers["slippage"])) if "slippage" in init_headers else 1
        self.buy_amount = 0
        self.sell_amount = 0
        self.apt_amount = 0

    def __setup_proxy(self, proxy: str):
        if proxy is None or proxy == "":
            self.logger.warning("All requests on the network will be without the use of a proxy")
            return None
        else:
            if len(proxy.split(":")) == 4:
                ip, port, user, passw = proxy.split(":")
                self.logger.info(f"using proxy http://{user}:{passw}@{ip}:{port}/")
                return f"http://{user}:{passw}@{ip}:{port}/"
            else:
                ip, port = proxy.split(":")
                self.logger.info(f"using proxy http://{ip}:{port}/")
                return f"http://{ip}:{port}/"

    def handle_one_task(self, step: dict) -> dict:
        try:
            self.logger.info(f"I received action {step}")
            status = self._handle_one_task(step)
            if status["code"] == 1:
                self.logger.info("Action completed successfully!")
            else:
                self.logger.error(f"Action failed {status}")
            return status
        except Exception as handler_exception:
            self.logger.error(handler_exception)
            return {"code": 19, "msg": ""}

    def _handle_one_task(self, step: dict) -> dict:
        for timing in TIMING:
            try:
                if step["action"] == "withdraw_okx":
                    amount = step["amount"]
                    if step["amount"] == "what_we_bought_on_okx":
                        amount = self.buy_amount
                    return self.handle_withdraw_okx(amount)
                if step["action"] == "swap":
                    save_to_apt = False if "save_balance" not in step else step["save_balance"]
                    return self.handle_swap(step["exchange"], step["swap_percent"], step["route"],
                                            save_to_apt=save_to_apt)
                if step["action"] == "sleep":
                    return self.handle_sleep(step["secs_amount"])
                if step["action"] == "transfer_to":
                    wait_for_deposit = True if "wait_for_deposit" not in step else step["wait_for_deposit"]
                    leave_on_funding = False if "leave_on_funding" not in step else step["leave_on_funding"]
                    return self.handle_transfer_to(step["amount"], step["address"], wait_for_deposit, leave_on_funding)
                if step["action"] == "all_token_to_apt":
                    return self.handle_all_token_to_apt()
                if step["action"] == "add_to_pool_with_apt":
                    return self.handle_add_to_pool(step["exchange"], step["token_percent"], step["token"])
                if step["action"] == "remove_from_pool_with_apt":
                    return self.handle_remove_from_all_pools(step["exchange"], step["token_percent"])
                if step["action"] == "buy_apt_on_okx":
                    return self.handle_buy_on_okx(step["amount"], stable=step["stable"])
                if step["action"] == "sell_apt_on_okx":
                    return self.handle_sell_on_okx(stable=step["stable"])
                if step["action"] in ["lending_deposit", "lending_withdraw"]:
                    return self.handle_lending(**step)
            except (SSLError, requests.exceptions.BaseHTTPError) as e:
                if step["action"] not in ["withdraw_okx", "buy_apt_on_okx", "sell_apt_on_okx", "transfer_to"]:
                    self.logger.info(f"I received SSLError. I will sleep {timing}")
                    self.handle_sleep(timing * 60)
                else:
                    raise e

    def handle_lending(self, action: str, lending: str, amount: str):
        tx = ""
        lendings = {
            "aptin": Aptin(self.eth_acc, proxy=self.proxy, user_agent=self.user_agent, logger=self.logger),
            "aries": Aries(self.eth_acc, proxy=self.proxy, user_agent=self.user_agent, logger=self.logger),
            "abel": AbelFinance(self.eth_acc, proxy=self.proxy, user_agent=self.user_agent, logger=self.logger)
        }
        try:
            if action == "lending_deposit":
                tx = lendings[lending].deposit_safe(Decimal(amount))
            elif action == "lending_withdraw":
                tx = lendings[lending].withdraw_safe(amount)
            time.sleep(4)
            tx_status = self.wallet_apt.get_transaction_status(tx)
            if not tx_status:
                return {"code": 14, "msg": f"Transaction rejected or not found. TXid: {tx}"}
            else:
                return {"code": 1, "msg": "OK"}
        except RuntimeError as lending_exception:
            self.logger.error(lending_exception)
            return {"code": 14, "msg": lending_exception.args}

    def handle_withdraw_okx(self, amount: str) -> dict:
        currencies = self.okx_account.get_currencies()
        balance = self.okx_account.get_balance()["APT"]
        fee = ""
        for chain in currencies["APT"]:
            if chain["chain"] == "APT-Aptos":
                fee = chain["minFee"]
        if amount == -1:
            amount = balance - Decimal(fee)
        elif Decimal(amount) - Decimal(fee) > balance:
            return {"code": 11,
                    "msg": f"Not enough money on okx! APT balance: {balance}, Request to withdraw: "
                           f"{Decimal(amount)} (fees included). Withdraw fee: {Decimal(fee)}"}
        elif Decimal(amount) - Decimal(fee) <= balance:
            amount = Decimal(amount) - Decimal(fee)
        balance_before_withdraw = self.wallet_apt.get_native_token_amount()
        start_time = time.time()

        while True:
            if self.event.is_set():
                return {'code': -1010, 'msg': 'Received a signal to stop the script and close the application'}
            wallet_balance = self.wallet_apt.get_native_token_amount()
            if balance_before_withdraw < wallet_balance:
                self.logger.info(f"transfer successful! wallet balance {Decimal(wallet_balance) / (10 ** 8)}")
                break
            else:
                self.logger.info(f"wait for withdraw for 10 minutes. balance {wallet_balance}")
                if time.time() - start_time > 60 * 20:
                    return {"code": 11, "msg": "We have problems with withdraw"}
            time.sleep(10)

        withdraw_action = {
            "project": "Aptos",
            "route": "WITHDRAW",
            "coin": "APT",
            "amount": Decimal(amount),
            "actions_time": datetime.datetime.fromtimestamp(time.time())
        }

        data = {
            "buy_action": None,
            "withdraw_action": withdraw_action,
            "deposit_action": None,
            "sell_action": None,
        }

        return {"code": 1, "msg": "OK", "data": data}

    def handle_transfer_to(self, amount: str, address: str, check_okx: bool, leave_on_funding: bool) -> dict:
        eth_before_deposit_to_okx = 0
        if check_okx:
            if self.okx_account.sub_account_name != "__main__":
                bal = self.okx_account.get_subaccount_balance(is_trading=False)
            else:
                bal = self.okx_account.get_trade_balance()
            if "APT" in bal:
                eth_before_deposit_to_okx = bal["APT"]
        max_amount = self.wallet_apt.calculate_max_transfer_amount(address)
        if "%" in amount:
            if amount == "100%":
                amount = max_amount
            else:
                amount = Decimal(int(Decimal(max_amount) / 100)) * int(amount.replace("%", ""))
        elif "leave" in amount:
            amount = max_amount - int(Decimal(amount.split("_")[1]) * 10 ** 8)
            if amount <= 0:
                raise RuntimeError("Not enough token for leave and deposit")
        else:
            if amount == "-1":
                amount = max_amount
            else:
                if Decimal(amount) * (10 ** 8) > max_amount:
                    return {"code": 16, "msg": f"You try send {amount} bigger "
                                               f"than max allowed {max_amount / (10 ** 8)}"}

        self.logger.info(f"I will transfer {amount} to {address}")
        self.logger.info("Transferring")
        tx = self.wallet_apt.transfer(address, amount)
        time.sleep(1)
        tx_status = self.wallet_apt.get_transaction_status(tx)

        if not tx_status:
            raise {"code": 16, "msg": f"Transaction rejected or not found. TXid: {tx}"}
        else:
            self.logger.info(f"Transaction successful! TXid: {tx}")
            if check_okx:
                self.logger.info("Checking OKX balance.")
                while True:
                    if self.event.is_set():
                        return {'code': -1010, 'msg': 'Received a signal to stop the script and close the application'}
                    if self.okx_account.sub_account_name != "__main__":
                        bal = self.okx_account.get_subaccount_balance(is_trading=False)
                    else:
                        bal = self.okx_account.get_trade_balance()
                    if "APT" in bal:
                        if eth_before_deposit_to_okx != bal["APT"]:
                            self.logger.info(
                                f"Deposit of {amount / (10 ** 8)} APT successful. APT amount: {bal['APT']}")
                            self.logger.info(f"Transferring {bal['APT']} APT to main account trading balance")
                            if self.okx_account.sub_account_name != "__main__":
                                self.okx_account.transfer_between_trading_and_funding_accounts(
                                    "APT", "funding_sub-trading_main", Decimal(amount) / (10 ** 8), True)
                            if leave_on_funding:
                                self.okx_account.transfer_between_trading_and_funding_accounts(
                                    "APT", "funding", Decimal(amount) / (10 ** 8), False)
                            if self.okx_account.sub_account_name == "__main__":
                                self.sell_amount = bal['APT'] - eth_before_deposit_to_okx
                            else:
                                self.sell_amount = bal['APT']

                            deposit_action = {
                                "project": "Aptos",
                                "route": "DEPOSIT",
                                "coin": "APT",
                                "amount": Decimal(self.sell_amount),
                                "actions_time": datetime.datetime.fromtimestamp(time.time())
                            }

                            data = {
                                "buy_action": None,
                                "withdraw_action": None,
                                "deposit_action": deposit_action,
                                "sell_action": None,
                            }

                            return {"code": 1, "msg": "OK", "data": data}
                        else:
                            self.logger.info(f"APT balance on okx: {bal['APT']} APT. "
                                             f"Wait for deposit. Refetch balances in 10 seconds")
                    else:
                        self.logger.info("APT balance on okx: 0 APT. Wait for deposit. Refetch balances in 10 seconds")
                    time.sleep(10)

    def handle_sleep(self, secs_amount: int) -> dict:
        wakeup_dt = datetime.datetime.fromtimestamp(time.time() + secs_amount)
        self.logger.info(f"I will sleep for {secs_amount} seconds. "
                         f"Wake up at {wakeup_dt.strftime('%d-%m-%Y %H:%M:%S')}")
        time.sleep(secs_amount)
        return {"code": 1, "msg": "OK"}

    def handle_swap(self, exchange: str, swap_percent: str | float, route: list, save_to_apt: bool) -> dict:
        if isinstance(swap_percent, str):
            if "%" in swap_percent:
                swap_percent = swap_percent.strip("%")
        if save_to_apt:
            self.apt_amount = self.wallet_apt.get_native_token_amount()
        if Decimal(str(swap_percent)) <= 0:
            self.logger.info(f"Skip swap {swap_percent}% {route[0]} on {exchange} to {route}")
            return {"code": 1, "msg": "OK"}
        self.logger.info(f"I will swap {swap_percent}% {route[0]} on {exchange} to {route}")
        exchanges = {
            "pancakeswap": PancakeSwap(self.eth_acc, proxy=self.proxy, slippage_tolerance=self.slippage,
                                       user_agent=self.user_agent, logger=self.logger),
            "liquidswap": LiquidSwap(self.eth_acc, proxy=self.proxy, slippage_tolerance=self.slippage,
                                     user_agent=self.user_agent, logger=self.logger),
        }
        use_exchange = exchanges[exchange]
        tx = use_exchange.exchange_with_amount_in_percent(Decimal(str(swap_percent)), route, self.apt_amount)
        time.sleep(4)
        tx_status = use_exchange.get_transaction_status(tx)
        if not tx_status:
            return {"code": 13, "msg": f"Transaction rejected or not found. TXid: {tx}"}
        else:
            self.logger.info(f"Transaction successful! TXid: {tx}")
            return {"code": 1, "msg": "OK"}

    def handle_add_to_pool(self, exchange: str, percent: str | float, token: str) -> dict:
        if Decimal(str(percent)) <= 0:
            self.logger.info(f"Skip adding liquidity {percent}% {token}/APT on {exchange}")
            return {"code": 1, "msg": "OK"}
        self.logger.info(f"I will add liquidity {percent}% {token}/APT on {exchange}")
        exchanges = {
            "pancakeswap": PancakeSwap(self.eth_acc, proxy=self.proxy, user_agent=self.user_agent, logger=self.logger),
            "liquidswap": LiquidSwap(self.eth_acc, proxy=self.proxy, user_agent=self.user_agent, logger=self.logger),
        }
        use_exchange = exchanges[exchange]
        tx = use_exchange.add_in_pool_for_apt_with_amount_in_percent(token, Decimal(str(percent)))
        time.sleep(4)
        tx_status = use_exchange.get_transaction_status(tx)
        if not tx_status:
            return {"code": 14, "msg": f"Transaction rejected or not found. TXid: {tx}"}
        else:
            self.logger.info(f"Transaction successful! TXid: {tx}")
            return {"code": 1, "msg": "OK"}

    def handle_remove_from_pool(self, exchange, percent, token):
        self.logger.info(f"I will remove liquidity {percent}% {token}/APT on {exchange}")
        exchanges = {
            "pancakeswap": PancakeSwap(self.eth_acc, proxy=self.proxy, user_agent=self.user_agent, logger=self.logger),
            "liquidswap": LiquidSwap(self.eth_acc, proxy=self.proxy, user_agent=self.user_agent, logger=self.logger),
        }
        use_exchange = exchanges[exchange]
        tx = use_exchange.remove_from_pool_for_apt_with_amount_in_percent(token, Decimal(str(percent)))
        time.sleep(4)
        if tx is None:
            self.logger.info("Skip this action")
        tx_status = use_exchange.get_transaction_status(tx)
        if not tx_status:
            return {"code": 14, "msg": f"Transaction rejected or not found. TXid: {tx}"}
        else:
            self.logger.info(f"Transaction successful! TXid: {tx}")
            return {"code": 1, "msg": "OK"}

    def handle_remove_from_all_pools(self, exchange: str, percent: str | float) -> dict:
        self.logger.info(f"I will remove liquidity {percent}% from all pools where I invested ob {exchange}")
        exchanges = {
            "pancakeswap": PancakeSwap(self.eth_acc, proxy=self.proxy, user_agent=self.user_agent, logger=self.logger),
            "liquidswap": LiquidSwap(self.eth_acc, proxy=self.proxy, user_agent=self.user_agent, logger=self.logger),
        }
        use_exchange = exchanges[exchange]
        for token in TOKENS:
            if token == "APT":
                continue
            self.logger.info(f"I will remove liquidity {percent}% {token}/APT on {exchange}")
            tx = use_exchange.remove_from_pool_for_apt_with_amount_in_percent(token, Decimal(str(percent)))
            time.sleep(4)
            if tx is None:
                self.logger.info("Skip this action")
            tx_status = use_exchange.get_transaction_status(tx)
            if not tx_status:
                return {"code": 14, "msg": f"Transaction rejected or not found. TXid: {tx}"}
            else:
                self.logger.info(f"Transaction successful! TXid: {tx}")
            self.handle_sleep(random.randint(20, 120))
        return {"code": 1, "msg": "OK"}

    def handle_buy_on_okx(self, usdt_amount: str | float, ticker: str = "APT", stable: str = "USDT") -> dict:
        self.logger.info(f"I going to buy APT for {usdt_amount} {stable} by market")
        try:
            order = self.okx_account.buy_by_market(usdt_amount, ticker, stable)
        except ConnectionError:
            self.logger.exception("")
            return {"code": 10, "msg": ""}

        self.logger.info(f"Buy success! Order info: {order}")
        self.logger.info("Requesting balance on trade account")
        trade_balances_snapshot = self.okx_account.get_trade_balance()
        self.logger.info(f"I will transfer {trade_balances_snapshot[ticker]} {ticker} to funding account")
        self.okx_account.transfer_between_trading_and_funding_accounts(ticker, "funding",
                                                                       trade_balances_snapshot[ticker])
        self.logger.info("Transfer success")
        self.buy_amount = Decimal(order["amount"]) + Decimal(order["fee"]) if (
                order["fee_currency"] == "APT") else Decimal(order["amount"])

        buy_action = {"route": "BUY", "eth_amount": Decimal(order["amount"]),
                      "price": Decimal(order["price"]), "coin": "ETH",
                      "usdt_amount": Decimal(order["quote_amount"]),
                      "actions_time": datetime.datetime.fromtimestamp(int(order["trade_time"]) / 1000)}
        data = {
            "buy_action": buy_action,
            "withdraw_action": None,
            "deposit_action": None,
            "sell_action": None,
        }

        return {"code": 1, "msg": "OK", "data": data}

    def handle_sell_on_okx(self, ticker: str = "APT", stable: str = "USDT") -> dict:
        self.logger.info(f"I going to sell all {ticker} for {stable} by market")
        self.logger.info(f"Selling {ticker} at market price")
        try:
            order = self.okx_account.sell_by_market(str(self.sell_amount), ticker, stable=stable)
        except Exception as sell_exception:
            self.logger.error(sell_exception)
            return {"code": 17, "msg": ""}

        self.logger.info(f"Sell success! Order info: {order}")
        sell_action = {"route": "SELL", "eth_amount": Decimal(order["amount"]),
                       "price": Decimal(order["price"]), "coin": "ETH",
                       "usdt_amount": Decimal(order["quote_amount"]),
                       "actions_time": datetime.datetime.fromtimestamp(int(order["trade_time"]) / 1000)}
        data = {
            "buy_action": None,
            "withdraw_action": None,
            "deposit_action": None,
            "sell_action": sell_action,
        }

        return {"code": 1, "msg": "OK", "data": data}

    def handle_all_token_to_apt(self) -> dict:
        pancake = PancakeSwap(self.eth_acc, proxy=self.proxy, slippage_tolerance=self.slippage,
                              user_agent=self.user_agent, logger=self.logger)
        for token in TOKENS:
            if self.event.is_set():
                return {'code': -1010, 'msg': 'Received a signal to stop the script and close the application'}
            if token == "APT":
                continue
            if self.wallet_apt.get_token_amount(TOKENS[token]) > 10:
                if pancake.is_swap_to_apt_covers_fee(TOKENS[token]):
                    swap_status = self.handle_swap("pancakeswap", 100, [token, "APT"], False)

                    if swap_status["code"] == 13:
                        return {"code": 13, "msg": f"Swap all amount {token} to APT failed: {swap_status}"}
                    self.handle_sleep(random.randint(40, 120))
                else:
                    self.logger.info(f"Swap {token} -> APT doesnt cover fee. Skip it")
        return {"code": 1, "msg": "OK"}
