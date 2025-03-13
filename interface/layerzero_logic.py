import datetime
import logging
import os
import random
import time
from threading import Thread, Event

from PySide6.QtCore import Signal, QObject

import layerzero.utils
from general_logger import OutputLogging
from layerzero.network.network import EVMNetwork
from layerzero.okx import Okx
from layerzero.spendlogic import Workflow
from utils import message_report_to_telegram


class LayerZero(QObject):
    tabFinish = Signal(str)
    tabClose = Signal(str, str)

    def __init__(self, accounts: list, ui: dict, output_field: QObject, tab_name: str, event: Event):
        super().__init__()
        self.ui = ui
        self.accounts = accounts
        self.output_field = output_field
        self.tab_name = tab_name
        self.event = event

        self.__logs_preparation()
        self.logger = logging.getLogger(self.tab_name)
        self.logger.handlers = []
        log_text_box = OutputLogging(self.output_field)
        log_formatter = logging.Formatter('%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s')
        log_text_box.setFormatter(log_formatter)
        self.logger.addHandler(log_text_box)
        self.logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler(f'logs/layer_zero/layer_zero_{datetime.date.today()}_'
                                           f'{datetime.datetime.now().hour}_'
                                           f'{datetime.datetime.now().minute}_'
                                           f'{datetime.datetime.now().second}.log')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(log_formatter)
        self.logger.addHandler(file_handler)

        self.in_work = False
        self.worker = None

    @staticmethod
    def __logs_preparation():
        if os.path.exists("logs/layer_zero"):
            pass
        else:
            os.makedirs("logs/layer_zero")

    def run(self):
        self.in_work = True
        self.worker = Thread(target=self.main, daemon=True, name=self.tab_name)
        self.worker.start()

    def __input_block_handler(self, header: dict, okx_instance: Okx) -> list[dict]:
        input_tasks = []

        random_decimals = random.randint(5, 8)
        amount = random.uniform(float(self.ui["input_min_field"]["text"]),
                                float(self.ui["input_max_field"]["text"]))
        amount = float(format(amount, f".{random_decimals}f"))
        input_tasks.append(
            {
                "action": "withdraw_from_okx",
                "params": {
                    "amount": amount,
                    "network": layerzero.utils.NETWORKS[self.ui["start_bridge_cb"]["text"]],
                    "address": layerzero.utils.get_address_from_private_key(header["pk"]),
                    "okx": okx_instance,
                    "token": self.ui["coin_selector"]["text"]
                }
            }
        )
        return input_tasks

    def __bridge_block_handler(self, header: dict, withdraw: bool = False,
                               withdraw_amount: float | None = None) -> tuple[list[dict], EVMNetwork]:
        all_tasks = []
        network_names = self.route_generator()
        networks_queue = layerzero.utils.get_networks_objects(network_names)

        all_tasks.append(
            {
                "action": "check_cost",
                "params": {
                    "networks": networks_queue.copy(),
                    "address": layerzero.utils.get_address_from_private_key(header["pk"])
                },
            }
        )

        start_network = networks_queue.pop(0)

        if withdraw:
            what_percent = "withdraw"
        else:
            what_percent = "wallet"

        for network in networks_queue:
            all_tasks.append(
                {
                    "action": "bridge",
                    "params": {
                        "key": header["pk"],
                        "address": layerzero.utils.get_address_from_private_key(header["pk"]),
                        "source_network": start_network,
                        "destination_network": network,
                        "max_stargate_fee": float(self.ui["max_stargate_fee_field"]["text"]),
                        "slippage": float(self.ui["slippage_field"]["text"]),
                        "percent_to_bridge": float(self.ui["percent_to_bridge_field"]["text"]),
                        "refuel_amount": None,
                        "what_percent": what_percent,
                        "withdraw_amount": withdraw_amount,
                        "token": self.ui["coin_selector"]["text"]
                    }
                }
            )
            start_network = network
        return all_tasks, start_network

    def __output_block_handler(self, header: dict, okx_instance: Okx, start_network: EVMNetwork) -> list[dict]:
        output_tasks = []

        random_decimals = random.randint(3, 8)
        amount = random.uniform(float(self.ui["output_min_field"]["text"]),
                                float(self.ui["output_max_field"]["text"]))
        amount = float(format(amount, f".{random_decimals}f"))
        output_tasks.append(
            {
                "action": "deposit_to_okx",
                "params": {
                    "private_key": header["pk"],
                    "okx": okx_instance,
                    "source_network": start_network,
                    "amount": amount,
                    "wallet": layerzero.utils.get_address_from_private_key(header["pk"]),
                    "address": header["okx_creds"]["deposit_address"]
                }
            }
        )

        return output_tasks

    def message_generator(self, times: list, header: dict) -> list[dict]:
        withdraw = False
        withdraw_amount = None
        okx_instance = Okx(header["okx_creds"]['api_key'], header["okx_creds"]['api_sec'],
                           header["okx_creds"]['api_pass'], header["okx_creds"]["sub_account_name"])

        self.logger.info("Try to generate task")
        tasks = []
        all_tasks = []

        if self.ui["input_okx_to_wallet_toggle"]["enabled"] and self.ui["input_okx_to_wallet_toggle"]["checked"]:
            input_task = self.__input_block_handler(header, okx_instance)
            tasks.extend(input_task)
            withdraw = True
            withdraw_amount = input_task[0]["params"]["amount"]

        bridge_tasks, last_network = self.__bridge_block_handler(header, withdraw, withdraw_amount)
        check_cost_message = bridge_tasks.pop(0)
        all_tasks.append(check_cost_message)
        tasks.extend(bridge_tasks)

        if self.ui["output_wallet_to_okx_toggle"]["enabled"] and self.ui["output_wallet_to_okx_toggle"]["checked"]:
            tasks.extend(self.__output_block_handler(header, okx_instance, last_network))

        for index, task in enumerate(tasks):
            all_tasks.append(
                {
                    "action": "check_gas_price",
                    "params": {
                        "network": layerzero.utils.NETWORKS['Ethereum'],
                        "max_value": float(self.ui["max_gas_fee_field"]["text"])
                    }
                }
            )
            all_tasks.append(task)
            all_tasks.append(
                {
                    "action": "sleep",
                    "params": times[index]
                }
            )
        return all_tasks

    def route_generator(self) -> list[str]:
        all_networks = []
        start_network = self.ui["start_bridge_cb"]["text"]
        finish_network = self.ui["finish_bridge_cb"]["text"]
        active_networks = self._get_active_networks()
        random.shuffle(active_networks)

        all_networks.append(start_network)
        all_networks.extend(active_networks)
        all_networks.append(finish_network)

        return all_networks

    def _get_active_networks(self) -> list[str]:
        active_networks = []
        if self.ui["arbitrum_toggle"]["enabled"] and self.ui["arbitrum_toggle"]["checked"]:
            active_networks.append("Arbitrum")
        if self.ui["optimism_toggle"]["enabled"] and self.ui["optimism_toggle"]["checked"]:
            active_networks.append("Optimism")
        if self.ui["base_toggle"]["enabled"] and self.ui["base_toggle"]["checked"]:
            active_networks.append("Base")
        if self.ui["linea_toggle"]["enabled"] and self.ui["linea_toggle"]["checked"]:
            active_networks.append("Linea")
        if self.ui["ethereum_toggle"]["enabled"] and self.ui["ethereum_toggle"]["checked"]:
            active_networks.append("Ethereum")
        if self.ui["avalanche_toggle"]["enabled"] and self.ui["avalanche_toggle"]["checked"]:
            active_networks.append("Avalanche")
        if self.ui["polygon_toggle"]["enabled"] and self.ui["polygon_toggle"]["checked"]:
            active_networks.append("Polygon")
        if self.ui["bsc_toggle"]["enabled"] and self.ui["bsc_toggle"]["checked"]:
            active_networks.append("Bsc")
        if self.ui["fantom_toggle"]["enabled"] and self.ui["fantom_toggle"]["checked"]:
            active_networks.append("Fantom")
        if self.ui["kava_toggle"]["enabled"] and self.ui["kava_toggle"]["checked"]:
            active_networks.append("Kava")
        return active_networks

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

    def count_optional_actions(self) -> int:
        optional_actions = 0
        if self.ui["send_avax_toggle"]["checked"]:
            optional_actions += 1
        if self.ui["send_matic_toggle"]["checked"]:
            optional_actions += 1
        if self.ui["send_ftm_toggle"]["checked"]:
            optional_actions += 1
        if self.ui["bsc_src_toggle"]["checked"]:
            if self.ui["coredao_bridge_toggle"]["checked"]:
                optional_actions += 1
        return optional_actions

    def count_actions(self) -> int:
        general_actions = 0
        if self.ui["input_okx_to_wallet_toggle"]["enabled"] and self.ui["input_okx_to_wallet_toggle"]["checked"]:
            general_actions += 1
        active_networks = self._get_active_networks()
        general_actions += len(active_networks) + 1
        if self.ui["output_wallet_to_okx_toggle"]["enabled"] and self.ui["output_wallet_to_okx_toggle"]["checked"]:
            general_actions += 1
        return general_actions

    def generate_tasks(self, account_data: dict) -> dict | None:
        if "proxy" in account_data:
            proxy = account_data['proxy']
        else:
            proxy = None
        all_message = {
            "header": {
                "pk": account_data['wallets']['EVM']['private_key'],
                "proxy": proxy,
                "pack": account_data['pack'],
                "event": self.event,
                "logger": self.logger,
                "gas_eth": int(self.ui["max_gas_fee_field"]["text"]),
                "slippage": float(self.ui["slippage_field"]["text"]),
                "stargate_fee": float(self.ui["max_stargate_fee_field"]["text"]),
                "okx_creds": {
                    "api_key": account_data['api_key'],
                    "api_sec": account_data['api_sec'],
                    "api_pass": account_data['api_passphrase'],
                    "sub_account_name": account_data["wallets"]["EVM"]["okx_subaccount"],
                    "deposit_address": account_data['wallets']['EVM']['okx_deposit_address']
                }
            }
        }
        range_time = self.get_range_time()
        messages = self.message_generator(range_time, all_message["header"])
        if messages is None:
            return None
        all_message['exchange_steps'] = messages
        return all_message

    def closing(self):
        self.logger.info("Close tab after:")
        for i in reversed(range(1, 6)):
            self.logger.info(f"{i}")
            time.sleep(1)

    def report(self, successful_accounts: list, failed_accounts: list, stop_pack: str = None, last_task: str = None):
        if stop_pack is None:
            if len(failed_accounts) == 0:
                self.logger.info(f"All accounts processing successfully.")
                sending_result = message_report_to_telegram(f"✅ Layer Zero || All accounts processing "
                                                            f"successfully: {successful_accounts}")
            else:
                self.logger.warning(f"Some accounts was FAILED: {failed_accounts}")
                sending_result = message_report_to_telegram(
                    f"⚠️ Layer Zero || Success accounts: {successful_accounts}; "
                    f"Failed accounts: {failed_accounts}")
        else:
            if len(failed_accounts) == 0:
                self.logger.info(f"Previous accounts processing successfully.")
                sending_result = message_report_to_telegram(f"✅ Layer Zero || Success accounts: {successful_accounts}."
                                                            f"Last account: {stop_pack}; last task: {last_task}")
            else:
                self.logger.warning(f"Some accounts was FAILED: {failed_accounts}")
                sending_result = message_report_to_telegram(
                    f"⚠️ Layer Zero || Success accounts: {successful_accounts}; "
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
                    if self.event.is_set():
                        self.closing()
                        break
                    self.logger.info("*" * 20)
                    self.logger.info(f"Processing pack {key['pack']}")

                    all_tasks = self.generate_tasks(key)
                    for task in all_tasks['exchange_steps']:
                        self.logger.info(task["action"])
                        if "withdraw_from_okx" in list(task.values()) or "deposit_to_okx" in list(task.values()):
                            withdraw_or_deposit = True

                    work = Workflow()
                    last_task = ""

                    for task in all_tasks['exchange_steps']:
                        if not stop_run and not skip_pack:
                            if self.event.is_set():
                                stop_run = True
                                self.closing()
                                self.report(successful_accounts, failed_accounts, key["pack"], last_task)
                                self.tabClose.emit(self.tab_name, "Layer Zero")
                                return -1

                            self.logger.info(task["action"])
                            time.sleep(5)

                            task["logger"] = self.logger
                            task["event"] = self.event

                            for handler in work.handlers:

                                result = handler.handle(task)
                                last_task = task["action"]
                                if result is not None:
                                    if int(result['code']) == 1:
                                        self.logger.info(result)

                                    elif int(result['code']) in [-1, 10, 11, 12, 16, 17, 19]:
                                        self.logger.error(f"Account {key['pack']} terminated with an error.")
                                        self.logger.error(result["msg"])
                                        failed_accounts.append(key['pack'])
                                        stop_run = True

                                    elif result['code'] == -1010:
                                        stop_run = True
                                        self.logger.warning(result)
                                        self.closing()
                                        self.report(successful_accounts, failed_accounts, key["pack"], last_task)
                                        self.tabClose.emit(self.tab_name, "Layer Zero")
                                        return -1

                                    elif result["code"] in [13, 14, 15]:
                                        failed_accounts.append(key['pack'])
                                        self.logger.warning(result)
                                        if withdraw_or_deposit:
                                            stop_run = True
                                            self.logger.warning(
                                                f"Account {key['pack']} has been terminated. "
                                                f"All accounts will be stopped")
                                        else:
                                            skip_pack = True
                                            self.logger.warning(
                                                f"Account {key['pack']} has been terminated and will be skipped")

                                    elif int(result["code"]) == 20:
                                        failed_accounts.append(key['pack'])
                                        self.logger.warning(result)
                                        skip_pack = True

                    self.logger.info(f"Account {key['pack']} finished work")
                    if key["pack"] not in failed_accounts:
                        successful_accounts.append(key["pack"])
                except Exception as run_exc:
                    self.logger.info(f"Account {key['pack']} ended prematurely. Status: FAILED")
                    self.logger.critical("An error occurred during the execution of the script")
                    self.logger.exception(run_exc)
                    failed_accounts.append(key['pack'])

        self.report(successful_accounts, failed_accounts)
        self.logger.info("*" * 20)
        self.in_work = False
        self.logger.handlers = []
        self.tabFinish.emit(self.tab_name)
