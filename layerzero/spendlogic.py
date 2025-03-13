import datetime
import random
import time
from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_DOWN

from layerzero.merkly.merkly_refuel import merkly_refuel, check_merkly_fees


class Handler(ABC):
    @abstractmethod
    def set_next(self, handler):
        pass

    @abstractmethod
    def handle(self, request):
        pass


class AbstractHandler(Handler):
    _next_handler: Handler = None

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, request):
        if self._next_handler:
            return self._next_handler.handle(request)

        return None


class WithdrawHandler(AbstractHandler):
    __okx_instance = None
    __network = None
    __stablecoin = None
    __amount = None
    __address = None
    __event = None
    __token = None
    logger = None

    def handle(self, request: dict) -> dict:
        if request['action'] == "withdraw_from_okx":
            self.logger = request['logger']
            self.__okx_instance = request['params']['okx']
            self.__network = request['params']['network']
            self.__amount = request['params']['amount']
            self.__address = request['params']['address']
            self.__event = request['event']
            self.__token = request['params']['token']
            self.__stablecoin = self.__network.supported_stable_coins[self.__token]
            return self._withdraw()
        else:
            return super().handle(request)

    def _withdraw(self):
        self.logger.info("Try make withdraw from OKX")
        currencies = self.__okx_instance.get_currencies()[self.__stablecoin.coin]
        for currency in currencies:
            if self.__event.is_set():
                return {'code': -1010, 'msg': 'Received a signal to stop the script and close the application'}
            if self.__network.name in currency['chain'].split('-')[1]:
                self.logger.info(f"From OKX to {self.__network.name}, amount: {self.__amount} "
                                 f"{self.__stablecoin.coin}")
                if self.__token == "ETH":
                    network_balance = self.__network.get_balance(self.__address)
                else:
                    network_balance = self.__network.get_token_balance(self.__stablecoin.contract_address,
                                                                       self.__address)
                withdraw_time = datetime.datetime.now()
                result = self.__okx_instance.withdraw(self.__stablecoin.coin, self.__amount, self.__address,
                                                      currency['minFee'], currency['chain'])

                self.logger.info(result.json())
                balance_changed = self.is_balance_changed(network_balance)
                if balance_changed['code'] == 1:
                    self.logger.info(result.json())
                    withdraw_action = {
                        "project": "Layer Zero",
                        "route": "WITHDRAW",
                        "coin": self.__stablecoin.coin,
                        "amount": self.__amount,
                        "actions_time": withdraw_time
                    }
                    data = {
                        "buy_action": None,
                        "withdraw_action": withdraw_action,
                        "deposit_action": None,
                        "sell_action": None,
                    }
                    return {"code": 1, "msg": balance_changed['msg'], "data": data}
                else:
                    return balance_changed

    def is_balance_changed(self, start_balance: int) -> dict:
        withdraw_status = False
        while not withdraw_status:
            if self.__event.is_set():
                return {'code': -1010, 'msg': 'Received a signal to stop the script and close the application'}

            self.logger.info("Waiting while balance will change")
            if self.__token == "ETH":
                current_network_balance = self.__network.get_balance(self.__address)
            else:
                current_network_balance = self.__network.get_token_balance(self.__stablecoin.contract_address,
                                                                           self.__address)
            if current_network_balance > start_balance:
                return {"code": 1, "msg": "Balance was changed. Withdrawal status: SUCCESS."}
            else:
                time.sleep(10)


class DepositHandler(AbstractHandler):
    __okx_instance = None
    __key = None
    __network = None
    __amount = None
    __address = None
    __stablecoin = None
    __wallet = None
    __event = None

    logger = None

    def handle(self, request: dict) -> dict:
        if request['action'] == "deposit_to_okx":
            self.logger = request['logger']
            self.__okx_instance = request['params']['okx']
            self.__key = request['params']['private_key']
            self.__network = request['params']['source_network']
            self.__amount = request['params']['amount']
            self.__address = request['params']['address']
            self.__wallet = request['params']['wallet']
            self.__event = request['event']
            if self.__network.name == "Optimism":
                self.__stablecoin = self.__network.supported_stable_coins['USDC']
            else:
                self.__stablecoin = self.__network.supported_stable_coins['USDT']
            return self._deposit()
        else:
            return super().handle(request)

    def _deposit(self):
        self.logger.info("Try make deposit to OKX")
        balance_before = self.__okx_instance.get_subaccount_balance(False)
        wallet_balance = self.__network.get_token_balance(self.__stablecoin.contract_address, self.__wallet)
        amount_for_deposit = int(wallet_balance - self.__amount * (10 ** self.__stablecoin.decimals))
        if self.__stablecoin.coin in list(balance_before.keys()):
            balance_before = balance_before[self.__stablecoin.coin]
        else:
            balance_before = 0
        deposit_datetime = datetime.datetime.now()
        if self.__event.is_set():
            return {'code': -1010, 'msg': 'Received a signal to stop the script and close the application'}

        deposit_result = self.__network.transfer(self.__key, self.__address, amount_for_deposit, self.__stablecoin)
        self.logger.info(f'Deposit result: {deposit_result.hex()}')
        balance_changed = self._is_balance_changed(balance_before)
        if balance_changed['code'] == 1:
            self._transfer_between_accounts(amount_for_deposit)
            self.logger.info("Transfer between accounts status: SUCCESS")
            deposit_action = {
                "project": "Layer Zero",
                "route": "DEPOSIT",
                "coin": self.__stablecoin.coin,
                "amount": amount_for_deposit / (10 ** self.__stablecoin.decimals),
                "actions_time": deposit_datetime
            }
            data = {
                "buy_action": None,
                "withdraw_action": None,
                "deposit_action": deposit_action,
                "sell_action": None,
            }
            return {"code": 1, "msg": balance_changed['msg'], "data": data}
        else:
            return balance_changed

    def _transfer_between_accounts(self, amount: int):
        time.sleep(10)
        self.__okx_instance.transfer_between_trading_and_funding_accounts(
            "USDT", "funding_sub-trading_main",
            Decimal(amount / (10 ** self.__stablecoin.decimals)).quantize(Decimal("1.00000000"), ROUND_DOWN), True)

        time.sleep(10)
        self.__okx_instance.transfer_between_trading_and_funding_accounts(
            "USDT", "funding",
            Decimal(amount / (10 ** self.__stablecoin.decimals)).quantize(Decimal("1.00000000"), ROUND_DOWN), False)

    def _is_balance_changed(self, start_balance: int) -> dict:
        withdraw_status = False
        while not withdraw_status:
            if self.__event.is_set():
                return {'code': -1010, 'msg': 'Received a signal to stop the script and close the application'}

            self.logger.info("Waiting while balance on OKX will change")
            current_okx_balance = self.__okx_instance.get_subaccount_balance(False)
            if self.__stablecoin.coin in list(current_okx_balance.keys()):
                coin_balance = current_okx_balance[self.__stablecoin.coin]
                if coin_balance > start_balance:
                    return {"code": 1, "msg": "Balance was changed. Deposit status: SUCCESS."}

            time.sleep(10)


class BridgeHandler(AbstractHandler):
    __source_network = None
    __destination_network = None
    __key = None
    __source_stablecoin = None
    __destination_stablecoin = None
    __address = None
    __max_stargate_fee = None
    _percent_type = None
    __token = None
    __event = None
    logger = None

    def handle(self, request: dict) -> dict:
        if request['action'] == "bridge":
            self.logger = request['logger']
            self.__source_network = request['params']['source_network']
            self.__destination_network = request['params']['destination_network']
            self.__key = request['params']['key']
            self.__address = request['params']['address']
            self.__max_stargate_fee = request['params']['max_stargate_fee']
            self._percent_type = request['params']['percent_type']
            self.__event = request['event']
            self.__token = request["params"]["token"]
            return self._bridge(request["params"])
        else:
            return super().handle(request)

    def _bridge(self, request: dict) -> dict:
        wallet_balance, start_destination_balance = self._get_balances()
        amount_to_bridge, amount_with_slippage = self._get_required_amount_to_bridge(request, wallet_balance)

        self.logger.info(f"Bridge {self.__source_network.name} {self.__source_stablecoin.coin} >> "
                         f"{self.__destination_network.name} {self.__destination_stablecoin.coin} "
                         f"amount: {amount_to_bridge / (10 ** self.__source_stablecoin.decimals)}")

        self.__is_enough_native_balance()
        self.__check_stargate_fee(amount_to_bridge)
        self.__source_network.approve_token_usage(self.__key, self.__source_stablecoin.contract_address,
                                                  self.__source_network.stargate_router_address, amount_to_bridge)
        try:
            if self.__token == "ETH":
                bridge_success = self.__source_network.make_stargate_eth_swap(
                    self.__key,
                    self.__destination_stablecoin.stargate_chain_id,
                    amount_to_bridge, amount_with_slippage,
                    request['refuel_amount']
                )
            else:
                bridge_success = self.__source_network.make_stargate_swap(
                    self.__key,
                    self.__destination_stablecoin.stargate_chain_id,
                    self.__source_stablecoin.stargate_pool_id,
                    self.__destination_stablecoin.stargate_pool_id,
                    amount_to_bridge, amount_with_slippage,
                    request['refuel_amount']
                )
        except ValueError as insufficient_balance_error:
            self.logger.error(insufficient_balance_error)
            return {"code": 20, "msg": "Insufficient balance"}

        if bridge_success[0]:
            self.logger.info(f"Hash: {bridge_success[1].hex()}")
            balance_changed = self._is_balance_changed(start_destination_balance, self.__token)
            if balance_changed:
                return {"code": 1, "msg": "Bridge status: SUCCESS"}
        return {"code": 12, "msg": "Bridge status: FAIL"}

    def _get_required_amount_to_bridge(self, request: dict, wallet_balance: int) -> tuple[int, int]:
        if self._percent_type == "wallet":
            self.logger.info("Use balance on wallet for bridge")
            amount_to_bridge = int(wallet_balance * (request['percent_to_bridge'] / 100))
        elif self._percent_type == "leave":
            if request['percent_to_bridge'] == "100%":
                amount_to_bridge = int(wallet_balance)
            elif (isinstance(request['percent_to_bridge'], str) and
                  request['params']['percent_to_bridge'].startswith("_")):
                amount_to_bridge = int(float(request['percent_to_bridge'].lstrip("_")) *
                                       (10 ** self.__source_stablecoin.decimals))
            else:
                amount_to_bridge = int(wallet_balance - request['percent_to_bridge'] *
                                       (10 ** self.__source_stablecoin.decimals))
        else:
            self.logger.info("Use withdraw amount for bridge")
            amount_gwei = request['withdraw_amount'] * (10 ** self.__source_stablecoin.decimals)
            amount_to_bridge = int(amount_gwei * (request['percent_to_bridge'] / 100))
        amount_with_slippage = amount_to_bridge - int(amount_to_bridge * (request['slippage'] / 100))
        return amount_to_bridge, amount_with_slippage

    def _get_balances(self) -> tuple[int, int]:
        if self.__token == "ETH":
            self.__source_stablecoin = self.__source_network.supported_stable_coins["ETH"]
            self.__destination_stablecoin = self.__destination_network.supported_stable_coins['ETH']
            wallet_balance = self.__source_network.get_balance(self.__address)
            start_destination_balance = self.__destination_network.get_balance(self.__address)
        else:
            supported_stables_source = self.__source_network.supported_stable_coins
            supported_stables_destination = self.__destination_network.supported_stable_coins
            supported_stables_source.pop("ETH", None)
            supported_stables_destination.pop("ETH", None)
            self.__source_stablecoin = random.choice(supported_stables_source)
            self.__destination_stablecoin = random.choice(supported_stables_destination)
            wallet_balance = self.__source_network.get_token_balance(self.__source_stablecoin.contract_address,
                                                                     self.__address)
            start_destination_balance = self.__destination_network.get_token_balance(
                self.__destination_stablecoin.contract_address, self.__address)
        return wallet_balance, start_destination_balance

    def __check_stargate_fee(self, amount: int) -> bool | dict:
        stargate_success = False
        while not stargate_success:
            if self.__event.is_set():
                return {'code': -1010, 'msg': 'Received a signal to stop the script and close the application'}

            stargate_fee = self.__source_network.estimate_stargate_fees(self.__source_stablecoin.stargate_pool_id,
                                                                        self.__destination_stablecoin.stargate_pool_id,
                                                                        self.__destination_network.stargate_chain_id,
                                                                        self.__address,
                                                                        amount,
                                                                        self.__source_stablecoin.decimals)
            self.logger.info(f"Stargate fee is: {stargate_fee}")
            if float(stargate_fee['sum_fee']) > float(self.__max_stargate_fee):
                self.logger.info("The amount of the stargate fee is too high. Waiting until the fee is less")
                time.sleep(10)
            else:
                return True

    def __is_enough_native_balance(self):
        self.logger.info(f"Check native token balance in {self.__source_network.name}")
        enough_balance = False
        while not enough_balance:
            if self.__event.is_set():
                return {'code': -1010, 'msg': 'Received a signal to stop the script and close the application'}

            account_balance = self.__source_network.get_balance(self.__address)
            gas_price = self.__source_network.estimate_swap_gas_price()
            layer_zero_fee = self.__source_network.estimate_layerzero_swap_fee(
                self.__destination_network.stargate_chain_id,
                self.__address)
            enough_native_token_balance = account_balance > (gas_price + layer_zero_fee)
            if enough_native_token_balance:
                self.logger.info("A native token is sufficient to complete a transaction")
                return {"code": 1, "msg": "A native token is sufficient to complete a transaction"}
            else:
                self.logger.warning(f"Not enough native token to complete a transaction. "
                                    f"Refill the balance of the native token ({self.__source_network.native_token})"
                                    f" on the network {self.__source_network.name}. On balance: {account_balance}; "
                                    f"required: {(gas_price + layer_zero_fee)}")
                time.sleep(30)

    def _is_balance_changed(self, start_balance: int, coin: str) -> dict:
        start_ts = datetime.datetime.now()
        withdraw_status = False
        while not withdraw_status:
            if self.__event.is_set():
                return {'code': -1010, 'msg': 'Received a signal to stop the script and close the application'}

            self.logger.info(f"Waiting while balance on {self.__destination_network.name} will change")
            if coin == "ETH":
                current_destination_balance = self.__destination_network.get_balance(self.__address)
            else:
                current_destination_balance = self.__destination_network.get_token_balance(
                    self.__destination_stablecoin.contract_address, self.__address)
            if current_destination_balance > start_balance:
                return {"code": 1, "msg": "Balance was changed. Bridge status: SUCCESS."}
            else:
                time.sleep(10)
                if (datetime.datetime.now() - start_ts).seconds == 600:
                    return {"code": 12, "msg": "Balance wasn't changed. Bridge status: FAIL."}


class SleepHandler(AbstractHandler):
    def handle(self, request: dict) -> dict:
        if request['action'] == "sleep":
            request['logger'].info(f"Sleep {request['params']} seconds. Wakeup "
                                   f"at {datetime.datetime.now() + datetime.timedelta(seconds=request['params'])}")
            time.sleep(request['params'])
            return {"code": 1, 'msg': "Wake up"}
        else:
            return super().handle(request)


class CoredaoHandler(AbstractHandler):
    def handle(self, request: dict) -> dict:
        if request['action'] == "coredao_bridge":
            request['logger'].info(f"Try make bridge to Core Dao. Route is BSC >> Core Dao."
                                   f" Amount: {request['params']['amount']}]")
            result = request['params']['network'].core_dao(request['params']['key'], request['params']['amount'])
            if result:
                return {"code": 1, "msg": "Bridge BSC >> Coredao. Status: SUCCESS"}
            else:
                return {"code": 12, "msg": "Bridge BSC >> Coredao. Status: FAIL"}
        else:
            return super().handle(request)


class CheckGasPriceHandler(AbstractHandler):
    def handle(self, request: dict) -> dict:
        if request['action'] == "check_gas_price":
            request['logger'].info("Check current gas price in Ethereum network")
            low_gas = False
            while not low_gas:
                gas_price = request['params']['network'].get_current_gas_eth()
                request['logger'].info(f"Current gas price {gas_price} GWEI.")
                if gas_price > request['params']['max_value']:
                    request['logger'].info("Current gas price is too high! Waiting for the price to come down")
                    time.sleep(20)
                else:
                    low_gas = True
            return {'code': 1, 'msg': "The current price is quite low. Still working"}
        else:
            return super().handle(request)


class CheckCostHandle(AbstractHandler):
    __networks = None
    __address = None
    logger = None

    def handle(self, request: dict) -> dict:
        if request['action'] == "check_cost":
            self.__networks = request['params']['networks']
            self.__address = request['params']['address']
            self.logger = request['logger']
            return self._check_cost(request)
        else:
            return super().handle(request)

    def _check_cost(self, request):
        all_route = ""
        required_index = 1
        need_to_refill = ""
        status_code = 1
        for i in range(0, len(self.__networks) - 1):
            if request['event'].is_set():
                return {'code': -1010, 'msg': 'Received a signal to stop the script and close the application'}

            source_network = self.__networks[required_index - 1]
            destination_network = self.__networks[required_index]
            account_balance = source_network.get_balance(self.__address)
            gas_price = source_network.estimate_swap_gas_price()
            layer_zero_fee = source_network.estimate_layerzero_swap_fee(destination_network.stargate_chain_id,
                                                                        self.__address)
            funds = gas_price + layer_zero_fee
            if account_balance > funds:
                all_route += f" || From {source_network.name} " \
                             f"to {destination_network.name} need " \
                             f"{funds / (10 ** source_network.native_decimals)} {source_network.native_token} " \
                             f"for gas. Wallet balance" \
                             f"is: {account_balance / (10 ** source_network.native_decimals)} " \
                             f"{source_network.native_token}"
                status_code = 1
            else:
                all_route += f" || <span style='color:#ff0000;'>From {source_network.name} " \
                             f"to {destination_network.name} need " \
                             f"{funds / (10 ** source_network.native_decimals)} {source_network.native_token} " \
                             f"for gas. Wallet balance" \
                             f"is: {account_balance / (10 ** source_network.native_decimals)} " \
                             f"{source_network.native_token}</span>"

                need_to_refill += f"{source_network.name} {source_network.native_token}. Mim amount " \
                                  f"{(funds - account_balance) / (10 ** source_network.native_decimals)} || "
                status_code = 20
            time.sleep(1)
            required_index += 1
        self.logger.info({'code': status_code, 'msg': all_route})
        return {'code': status_code, "msg": f"Need to refuel: <span style='color:#ff0000;'>{need_to_refill}</span>"}


class MerklyRefuelHandler(AbstractHandler):
    __source_network = None
    __destination_network = None
    __key = None
    __event = None
    logger = None
    __address = None

    def handle(self, request: dict) -> dict:
        if request['action'] == "merkly_refuel":
            self.logger = request['logger']
            self.__source_network = request['params']['source_network']
            self.__destination_network = request['params']['destination_network']
            self.__key = request['params']['key']
            self.__event = request['event']
            self.__address = request['params']['address']
            return self._merkly_refuel(request['params']['amount'])

        else:
            return super().handle(request)

    def _merkly_refuel(self, amount: int) -> dict:
        check_native_balance = self.__is_enough_native_balance()
        if check_native_balance['code'] == -1010:
            self.logger.warning(check_native_balance)
            return check_native_balance
        elif check_native_balance['code'] == 1:
            self.logger.info(check_native_balance)

        self.logger.info(f"Try bridge native token between {self.__source_network.name} "
                         f"and {self.__destination_network.name} (Expected output: {amount} "
                         f"{self.__destination_network.native_token}).")
        refuel_result = merkly_refuel(self.__key, self.__source_network, self.__destination_network, amount)
        return refuel_result

    def __is_enough_native_balance(self):
        self.logger.info(f"Check native token balance in {self.__source_network.name}")
        enough_balance = False

        while not enough_balance:
            if self.__event.is_set():
                return {'code': -1010, 'msg': 'Received a signal to stop the script and close the application'}

            account_balance = self.__source_network.get_balance(self.__address)
            gas_price = self.__source_network.estimate_swap_gas_price()
            self.logger.info("Check refuel cost.")
            refuel_cost = check_merkly_fees(self.__source_network, self.__destination_network, self.__key)
            if refuel_cost['code'] == 1:
                self.logger.info(refuel_cost['msg'])
            else:
                self.logger.error(refuel_cost)
            enough_native_token_balance = account_balance > (gas_price + refuel_cost['data'])
            if enough_native_token_balance:
                self.logger.info("A native token is sufficient to complete a transaction")
                return {"code": 1, "msg": "A native token is sufficient to complete a transaction"}
            else:
                self.logger.warning(f"Not enough native token to complete a transaction. "
                                    f"Refill the balance of the native token ({self.__source_network.native_token})"
                                    f" on the network {self.__source_network.name}. On balance: {account_balance}; "
                                    f"required: {(gas_price + refuel_cost['data'])}")
                time.sleep(30)


class Workflow(object):
    def __init__(self):
        self.handlers = [
            WithdrawHandler(),
            DepositHandler(),
            BridgeHandler(),
            SleepHandler(),
            CoredaoHandler(),
            CheckGasPriceHandler(),
            CheckCostHandle(),
            MerklyRefuelHandler()
        ]

    def start(self, tasks):
        for task in tasks:
            for h in self.handlers:
                result = h.handle(task)
                if result is not None:
                    return result

        return -1
