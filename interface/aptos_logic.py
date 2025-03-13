import datetime
import logging
import os
import random
import time
from threading import Thread, Event

from PySide6.QtCore import Signal, QObject

from aptos.spendlogic import Spendlogic
from general_logger import OutputLogging
from utils import message_report_to_telegram


class Aptos(QObject):
    coins = {
        "APT": ["USDT", "USDC"],
        "USDT": ["USDC", "APT"],
        "USDC": ["USDT", "APT"],
    }

    tabFinish = Signal(str)
    tabClose = Signal(str, str)

    def __init__(self, accounts: list, ui: dict, output_field: QObject, tab_name: str, event: Event):
        super().__init__()
        self.ui = ui
        self.accounts = accounts
        self.output_field = output_field
        self.tab_name = tab_name

        self.__logs_preparation()
        self.logger = logging.getLogger(self.tab_name)
        self.logger.handlers = []
        log_text_box = OutputLogging(self.output_field)
        log_formatter = logging.Formatter('%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s')
        log_text_box.setFormatter(log_formatter)
        self.logger.addHandler(log_text_box)
        self.logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler(f'logs/aptos/aptos_{datetime.date.today()}_'
                                           f'{datetime.datetime.now().hour}_'
                                           f'{datetime.datetime.now().minute}_'
                                           f'{datetime.datetime.now().second}.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(log_formatter)
        self.logger.addHandler(file_handler)

        self.filename = ""
        self.in_work = False
        self.event = event

    @staticmethod
    def __logs_preparation():
        if os.path.exists("logs/aptos"):
            pass
        else:
            os.makedirs("logs/aptos")

    def run(self):
        self.in_work = True
        t = Thread(target=self.main, daemon=True, name=self.tab_name)
        t.start()

    def generate_tasks(self, account_data: dict) -> dict:
        if "proxy" in account_data:
            proxy = account_data['proxy']
        else:
            proxy = None
        all_message = {
            "header": {
                "pk": account_data['wallets']['APTOS']['private_key'],
                "proxy": proxy,
                "pack": account_data['pack'],
                "event": self.event,
                "logger": self.logger,
                "slippage": float(self.ui["slippage_field"]["text"]),
                "okx_creds": {
                    "api_key": account_data['api_key'],
                    "api_sec": account_data['api_sec'],
                    "api_pass": account_data['api_passphrase'],
                    "sub_account_name": account_data["wallets"]["APTOS"]["okx_subaccount"]
                }
            }
        }
        range_time = self.get_range_time()
        messages = self.message_generator(range_time, account_data['wallets']['APTOS']['okx_deposit_address'])
        all_message['exchange_steps'] = messages
        return all_message

    def get_random_routes(self) -> list[list[str, list[str, str], float | str]]:
        routes = []
        active_swap = self.__get_active_swap("swap")
        previous_coin = "APT"
        random.shuffle(active_swap)

        if self.ui["one_of_all_toggle"]["checked"]:
            swap = random.choice(active_swap)
            swap_stables = self.coins[previous_coin]
            random.shuffle(swap_stables)
            required_stable = random.choice(swap_stables)
            random_decimals = random.randint(3, 8)
            swap_percent = random.uniform(float(self.ui["swap_min_field"]["text"]),
                                          float(self.ui["swap_max_field"]["text"]))
            swap_percent = float(format(swap_percent, f".{random_decimals}f"))
            routes.append([swap, [previous_coin, required_stable], swap_percent])
            return routes

        counter = len(active_swap)
        while counter > 0:
            swap = random.choice(active_swap)
            swap_stables = self.coins[previous_coin]
            random.shuffle(swap_stables)
            required_stable = random.choice(swap_stables)
            if previous_coin == "APT":
                random_decimals = random.randint(3, 8)
                swap_percent = random.uniform(float(self.ui["swap_min_field"]["text"]),
                                              float(self.ui["swap_max_field"]["text"]))
                swap_percent = float(format(swap_percent, f".{random_decimals}f"))
            else:
                swap_percent = "100%"
            routes.append([swap, [previous_coin, required_stable], swap_percent])

            active_swap.remove(swap)
            counter = len(active_swap)
            previous_coin = required_stable

        return routes

    def __get_active_swap(self, block: str) -> list[str]:
        if block == "swap":
            active_swap = []
            if self.ui["swap_pancakeswap_toggle"]["checked"]:
                active_swap.append("pancakeswap")
            if self.ui["swap_liquidswap_toggle"]["checked"]:
                active_swap.append("liquidswap")
            return active_swap
        elif block == "pool":
            active_pool = []
            if self.ui["pool_pancakeswap_toggle"]["checked"]:
                active_pool.append("pancakeswap")
            if self.ui["pool_liquidswap_toggle"]["checked"]:
                active_pool.append("liquidswap")
            return active_pool

    def __input_block_handler(self) -> list[dict]:
        input_tasks = []
        if self.ui["coin_selector"]["enabled"]:
            input_coin = self.ui["coin_selector"]["text"]
        else:
            input_coin = None

        if input_coin is not None:
            random_decimals = random.randint(3, 8)
            amount = random.uniform(float(self.ui["input_min_field"]["text"]),
                                    float(self.ui["input_max_field"]["text"]))
            amount = float(format(amount, f".{random_decimals}f"))
            if input_coin == "USDT" or input_coin == "USDC":
                input_tasks.append(
                    {
                        "action": "buy_apt_on_okx",
                        "amount": amount,
                        "stable": input_coin
                    }
                )
                amount_to_withdraw = "what_we_bought_on_okx"
            else:
                amount_to_withdraw = f"{amount}"

        if self.ui["input_okx_to_aptos_bridge_toggle"]["checked"]:
            network = "aptos"
        else:
            network = None

        if network is not None:
            input_tasks.append(
                {
                    "action": "withdraw_okx",
                    "amount": amount_to_withdraw,
                    "network": network
                }
            )
        return input_tasks

    def __swap_block_handler(self) -> list[dict]:
        swap_tasks = []
        counter = 0
        active_pools_amount = 0

        if int(self.ui["swap_iteration_field"]["text"]) > 0:
            for i in range(0, int(self.ui["swap_iteration_field"]["text"])):
                try:
                    routes = self.get_random_routes()
                except ValueError as routes_error:
                    self.logger.error(routes_error, exc_info=True)
                    return []
                if self.ui["pool_enable_toggle"]["checked"]:
                    pool_tasks = self.__pool_block_handler()
                    active_pools_amount = len(list(pool_tasks.keys()))
                for index, route in enumerate(routes):
                    if (self.ui["pool_enable_toggle"]["checked"] and counter <
                            int(self.ui["pool_iteration_field"]["text"]) * int(active_pools_amount / 2)):
                        if route[1][1] == "APT":
                            required_token = route[1][0]
                        else:
                            required_token = route[1][1]
                        pool_task_add = pool_tasks.pop(f"{route[0]}_add", False)
                        pool_task_remove = pool_tasks.pop(f"{route[0]}_remove", False)
                        if route[-1] == 100:
                            route[-1] = 99
                        message_swap = {
                            "action": "swap",
                            "exchange": route[0],
                            "route": route[1],
                            "swap_percent": route[-1],
                            "save_balance": False
                        }
                        swap_tasks.append(message_swap)
                        if pool_task_add:
                            pool_task_add["token"] = required_token
                            swap_tasks.append(pool_task_add)
                        if pool_task_remove:
                            pool_task_remove["token"] = required_token
                            swap_tasks.append(pool_task_remove)
                        if pool_task_add or pool_task_remove:
                            counter += 1
                    else:
                        if route[-1] == 100:
                            route[-1] = 99
                        message_swap = {
                            "action": "swap",
                            "exchange": route[0],
                            "route": route[1],
                            "swap_percent": route[-1],
                            "save_balance": False
                        }
                        swap_tasks.append(message_swap)
        else:
            if self.ui["pool_enable_toggle"]["checked"]:
                pool_tasks = self.__pool_block_handler()
                swap_tasks.extend(pool_tasks.values())
        return swap_tasks

    def __pool_block_handler(self):
        pool_tasks = {}
        active_swap = self.__get_active_swap("pool")
        for swap in active_swap:
            if self.ui["pool_add_min_field"]["text"] not in ["", "0"]:
                add_amount = random.uniform(float(self.ui["pool_add_min_field"]["text"]),
                                            float(self.ui["pool_add_max_field"]["text"]))
                pool_tasks[f"{swap}_add"] = {
                    "action": "add_to_pool_with_apt",
                    "exchange": swap,
                    "token_percent": add_amount
                }

            if self.ui["pool_remove_min_field"]["text"] not in ["", "0"]:
                remove_amount = random.uniform(float(self.ui["pool_remove_min_field"]["text"]),
                                               float(self.ui["pool_remove_max_field"]["text"]))
                pool_tasks[f"{swap}_remove"] = {
                    "action": "remove_from_pool_with_apt",
                    "exchange": swap,
                    "token_percent": remove_amount
                }
        return pool_tasks

    def __lending_block_handler(self) -> list[dict]:
        lending_tasks = []
        active_lending = []
        if self.ui["lending_aptin_toggle"]["checked"]:
            active_lending.append("aptin")
        if self.ui["lending_aries_toggle"]["checked"]:
            active_lending.append("aries")
        if self.ui["lending_abel_finance_toggle"]["checked"]:
            active_lending.append("abel")
        for i in range(0, int(self.ui["lending_iteration_field"]["text"])):
            random.shuffle(active_lending)
            for lending in active_lending:
                if self.ui["lending_add_min_field"]["text"] not in ["", "0"]:
                    random_decimals = random.randint(3, 8)
                    add_amount = random.uniform(float(self.ui["lending_add_min_field"]["text"]),
                                                float(self.ui["lending_add_max_field"]["text"]))
                    add_amount = float(format(add_amount, f".{random_decimals}f"))
                    lending_tasks.append(
                        {
                            "action": "lending_deposit",
                            "lending": lending,
                            "amount": add_amount
                        }
                    )

                if self.ui["lending_remove_all_toggle"]["checked"]:
                    lending_tasks.append(
                        {
                            "action": "lending_withdraw",
                            "lending": lending,
                            "amount": "100%"
                        }
                    )
                else:
                    if self.ui["lending_remove_min_field"]["text"] not in ["", "0"]:
                        remove_amount = random.uniform(float(self.ui["lending_remove_min_field"]["text"]),
                                                       float(self.ui["lending_remove_max_field"]["text"]))
                        lending_tasks.append(
                            {
                                "action": "lending_withdraw",
                                "lending": lending,
                                "amount": remove_amount
                            }
                        )
        return lending_tasks

    def __output_block_handler(self, address: str) -> list[dict]:
        output_tasks = []

        if self.ui["output_aptos_to_okx_toggle"]["checked"]:
            network = "aptos"
        else:
            network = None

        amount = random.uniform(float(self.ui["output_min_field"]["text"]),
                                float(self.ui["output_max_field"]["text"]))

        if network is not None:
            output_tasks.append(
                {
                    "action": "transfer_to",
                    "amount": f"leave_{amount}",
                    "address": address,
                    "network": network,
                    "wait_for_deposit": True,
                }
            )
            if self.ui["output_sell_apt_toggle"]["enabled"]:
                if self.ui["output_sell_apt_toggle"]["checked"]:
                    output_tasks.append(
                        {
                            "action": "sell_apt_on_okx",
                            "stable": "USDC"
                        }
                    )
        return output_tasks

    def message_generator(self, times: list, address_to: str) -> list[dict]:
        self.logger.info("Try to generate task")
        tasks = []
        all_tasks = []
        swap_tasks = []
        lending_tasks = []

        if self.ui["input_okx_to_aptos_bridge_toggle"]["checked"]:
            tasks.extend(self.__input_block_handler())

        if self.ui["swap_enable_toggle"]["checked"]:
            swap_tasks.extend(self.__swap_block_handler())

        if self.ui["lending_enable_toggle"]["checked"]:
            lending_tasks.extend(self.__lending_block_handler())

        if len(lending_tasks) > 0:
            if len(lending_tasks) == 2:
                last_lending_task = lending_tasks.pop(-1)
                lending_tasks.extend(swap_tasks)
                lending_tasks.append(last_lending_task)
            elif len(lending_tasks) == 1:
                lending_tasks.extend(swap_tasks)
            else:
                lending_tasks_copy = lending_tasks.copy()
                lending_tasks.clear()
                for index in range(0, max(len(swap_tasks), len(lending_tasks_copy))):
                    try:
                        lending_tasks.append(lending_tasks_copy[index])
                    except IndexError:
                        pass
                    try:
                        if (index <= len(lending_tasks_copy) - 1 and
                                lending_tasks_copy[index]["action"] == "lending_deposit"):
                            swap_tasks[index]["save_balance"] = True
                            lending_tasks.append(swap_tasks[index])
                        else:
                            lending_tasks.append(swap_tasks[index])
                    except IndexError:
                        pass
            tasks.extend(lending_tasks)
        else:
            tasks.extend(swap_tasks)

        if self.ui["all_to_apt_toggle"]["checked"]:
            tasks.append(
                {
                    "action": "all_token_to_apt"
                }
            )

        if self.ui["output_aptos_to_okx_toggle"]["checked"]:
            tasks.extend(self.__output_block_handler(address_to))

        for index, task in enumerate(tasks):
            all_tasks.append(task)
            all_tasks.append(
                {
                    "action": "sleep",
                    "secs_amount": times[index]
                }
            )
        return all_tasks

    def get_range_time(self) -> list[int]:
        correct_time = False
        actions_quantity = self.count_actions()
        time_for_sleep = []
        if self.ui["asap_toggle"]["checked"]:
            for i in range(0, actions_quantity + 3):
                time_for_sleep.append(1)
            return time_for_sleep

        time_from = (int(self.ui["time_from_field"]["text"].split(":")[0]) * 60 + int(
            self.ui["time_from_field"]["text"].split(":")[1])) * 60
        time_to = (int(self.ui["time_to_field"]["text"].split(":")[0]) * 60 + int(
            self.ui["time_to_field"]["text"].split(":")[1])) * 60
        general_time_minute = random.randint(time_from, time_to)
        while not correct_time:
            samples = [random.randrange(general_time_minute + 1)
                       for _ in range(actions_quantity - 1)] + [0, general_time_minute]
            samples.sort()
            time_for_sleep = [b - a for a, b in zip(samples[:-1], samples[1:])]
            if 0 not in time_for_sleep:
                correct_time = True
        random.shuffle(time_for_sleep)
        return time_for_sleep

    def count_actions(self) -> int:
        general_actions = 0
        if self.ui["input_okx_to_aptos_bridge_toggle"]["checked"]:
            if self.ui["coin_selector"]["text"] == "APT" or not self.ui["coin_selector"]["enabled"]:
                general_actions += 2
            else:
                general_actions += 3

        if self.ui["swap_enable_toggle"]["checked"]:
            if self.ui["one_of_all_toggle"]["checked"]:
                general_actions += int(self.ui["swap_iteration_field"]["text"])
            else:
                general_actions += len(self.__get_active_swap("swap")) * int(self.ui["swap_iteration_field"]["text"])
            if self.ui["all_to_apt_toggle"]["checked"]:
                general_actions += 1
        if self.ui["pool_enable_toggle"]["checked"]:
            if self.ui["one_of_all_toggle"]["checked"]:
                if self.ui["pool_add_min_field"]["text"] not in ["", "0"]:
                    general_actions += int(self.ui["pool_iteration_field"]["text"])
                if self.ui["pool_remove_min_field"]["text"] not in ["", "0"]:
                    general_actions += int(self.ui["pool_iteration_field"]["text"])
            else:
                active_pools = self.__get_active_swap("pool")
                if self.ui["pool_add_min_field"]["text"] not in ["", "0"]:
                    general_actions += len(active_pools) * int(self.ui["pool_iteration_field"]["text"])
                if self.ui["pool_remove_min_field"]["text"] not in ["", "0"]:
                    general_actions += len(active_pools) * int(self.ui["pool_iteration_field"]["text"])

        if self.ui["lending_enable_toggle"]["checked"]:
            active_lending = []
            if self.ui["lending_aptin_toggle"]["checked"]:
                active_lending.append("aptin")
            if self.ui["lending_aries_toggle"]["checked"]:
                active_lending.append("aries")
            if self.ui["lending_abel_finance_toggle"]["checked"]:
                active_lending.append("abel_finance")

            if self.ui["lending_add_min_field"]["text"] not in ["", "0"]:
                general_actions += len(active_lending) * int(self.ui["lending_iteration_field"]["text"])
            if (self.ui["lending_remove_min_field"]["text"] not in ["", "0"] or
                    self.ui["lending_remove_all_toggle"]["checked"]):
                general_actions += len(active_lending) * int(self.ui["lending_iteration_field"]["text"])

        if self.ui["output_aptos_to_okx_toggle"]["checked"]:
            general_actions += 1
            if self.ui["output_sell_apt_toggle"]["checked"]:
                general_actions += 1
        return general_actions

    def closing(self):
        self.logger.info("Close tab after:")
        for i in reversed(range(1, 6)):
            self.logger.info(f"{i}")
            time.sleep(1)

    def report(self, successful_accounts: list, failed_accounts: list, stop_pack: str = None, last_task: str = None):
        if stop_pack is None:
            if len(failed_accounts) == 0:
                self.logger.info(f"All accounts processing successfully.")
                sending_result = message_report_to_telegram(f"✅ Aptos || All accounts processing "
                                                            f"successfully: {successful_accounts}")
            else:
                self.logger.warning(f"Some accounts was FAILED: {failed_accounts}")
                sending_result = message_report_to_telegram(f"⚠️ Aptos || Success accounts: {successful_accounts}; "
                                                            f"Failed accounts: {failed_accounts}")
        else:
            if len(failed_accounts) == 0:
                self.logger.info(f"Previous accounts processing successfully.")
                sending_result = message_report_to_telegram(f"✅ Aptos || Success accounts: {successful_accounts}."
                                                            f"Last account: {stop_pack}; last task: {last_task}")
            else:
                self.logger.warning(f"Some accounts was FAILED: {failed_accounts}")
                sending_result = message_report_to_telegram(f"⚠️ Aptos || Success accounts: {successful_accounts}; "
                                                            f"Failed accounts: {failed_accounts}"
                                                            f"Last account: {stop_pack}; last task: {last_task}")

        if "code" in sending_result:
            if sending_result["code"] == -1:
                self.logger.warning(sending_result)

    def check_schedule(self):
        if self.ui["datetime_schedule"]["enabled"]:
            datetime_string = self.ui["datetime_schedule"]["text"]
            current_datetime = datetime.datetime.now()
            schedule_datetime = datetime.datetime.strptime(datetime_string, "%d.%m.%Y %H:%M")

            if current_datetime < schedule_datetime:
                time_to_sleep = (schedule_datetime - current_datetime).seconds
                self.logger.info(f"You set the script to run on {datetime_string}")
                time.sleep(time_to_sleep)
            else:
                self.logger.warning("The delayed start of the script is impossible because you have "
                                    "specified a time that is less than the current one!")
                self.tabFinish.emit(self.tab_name)
                return -1

    def main(self):
        self.check_schedule()
        failed_accounts = []
        successful_accounts = []
        stop_run = False
        withdraw_or_deposit = False

        for key in self.accounts:
            skip_pack = False
            if not stop_run:
                try:
                    self.logger.info("*" * 20)
                    self.logger.info(f"Processing pack {key['pack']}.")
                    all_tasks = self.generate_tasks(key)
                    for task in all_tasks['exchange_steps']:
                        self.logger.info(task)
                        if "withdraw_okx" in list(task.values()) or "transfer_to" in list(task.values()):
                            withdraw_or_deposit = True

                    header = all_tasks['header']
                    sl = Spendlogic(header)
                    last_task = ""

                    for task in all_tasks['exchange_steps']:
                        if not stop_run and not skip_pack:
                            if self.event.is_set():
                                stop_run = True
                                self.closing()
                                self.report(successful_accounts, failed_accounts, key["pack"], last_task)
                                self.tabClose.emit(self.tab_name, "Aptos")
                                return -1

                            self.logger.info(task)
                            result = sl.handle_one_task(task)
                            last_task = task
                            if int(result['code']) == 1:
                                self.logger.info(result)

                            elif int(result['code']) in [-1, 10, 11, 12, 16, 17, 19]:
                                self.logger.error(f"Account {key['pack']} terminated with an error.")
                                self.logger.error(result)
                                failed_accounts.append(key['pack'])
                                stop_run = True
                            elif result['code'] == -1010:
                                stop_run = True
                                self.logger.warning(result)
                                self.closing()
                                self.report(successful_accounts, failed_accounts, key["pack"], last_task)
                                self.tabClose.emit(self.tab_name, "Aptos")
                                return -1

                            elif result["code"] in [13, 14, 15]:
                                failed_accounts.append(key['pack'])
                                self.logger.warning(result)
                                if withdraw_or_deposit:
                                    stop_run = True
                                    self.logger.warning(
                                        f"Account {key['pack']} has been terminated. All accounts will be stopped")
                                else:
                                    skip_pack = True
                                    self.logger.warning(
                                        f"Account {key['pack']} has been terminated and will be skipped")

                            elif int(result["code"]) == 20:
                                failed_accounts.append(key['pack'])
                                self.logger.warning(result)
                                skip_pack = True
                            else:
                                self.logger.warning(f"Unknown result: {result}")

                    self.logger.info(f"Account {key['pack']} finished work")
                    if key["pack"] not in failed_accounts:
                        successful_accounts.append(key["pack"])
                except Exception as run_exc:
                    self.logger.error(f"Account {key['pack']} ended prematurely. Status: FAILED")
                    self.logger.critical("An error occurred during the execution of the script")
                    self.logger.exception(run_exc)
                    failed_accounts.append(key['pack'])

        self.report(successful_accounts, failed_accounts)
        self.logger.info("*" * 20)
        self.in_work = False
        self.logger.handlers = []
        self.tabFinish.emit(self.tab_name)
