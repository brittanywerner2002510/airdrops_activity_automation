import datetime
import logging
import os
import random
import time
from threading import Thread, Event

from PySide6.QtCore import Signal, QObject

import layerzero.utils
from general_logger import OutputLogging
from layerzero.spendlogic import Workflow
from utils import message_report_to_telegram


class Merkly(QObject):
    tabFinish = Signal(str)
    tabClose = Signal(str, str)

    def __init__(self, accounts: list, ui: dict, output_field: QObject, tab_name: str, event: Event):
        super().__init__()
        self.ui = ui
        self.accounts = accounts
        self.source_networks = []
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
        file_handler = logging.FileHandler(f'logs/merkly/merkly_{datetime.date.today()}_'
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
        if os.path.exists("logs/merkly"):
            pass
        else:
            os.makedirs("logs/merkly")

    def run(self):
        self.in_work = True
        self.worker = Thread(target=self.main, daemon=True, name=self.tab_name)
        self.worker.start()

    def get_range_time(self) -> list[int]:
        correct_time = False
        actions_quantity = 1
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

    def message_generator(self, key: str, address: str) -> list[dict]:
        all_tasks = []
        amount_to_bridge = random.uniform(float(self.ui["input_min_field"]["text"]),
                                          float(self.ui["input_max_field"]["text"]))
        times = self.get_range_time()

        if self.ui["max_gas_fee_field"]["enabled"]:
            all_tasks.append(
                {
                    "action": "check_gas_price",
                    "params": {
                        "network": layerzero.utils.NETWORKS['Ethereum'],
                        "max_value": float(self.ui["max_gas_fee_field"]["text"])
                    }
                }
            )

        all_tasks.append(
            {
                "action": "merkly_refuel",
                "params": {
                    "source_network": layerzero.utils.NETWORKS[self.ui["source_network_cb"]["text"]],
                    "destination_network": layerzero.utils.NETWORKS[
                        self.ui["destination_network_cb"]["text"]],
                    "amount": amount_to_bridge,
                    "key": key,
                    "address": address
                },
            }
        )
        all_tasks.append(
            {
                "action": "sleep",
                "params": times[0]
            }
        )
        return all_tasks

    def closing(self):
        self.logger.info("Close tab after:")
        for i in reversed(range(1, 6)):
            self.logger.info(f"{i}")
            time.sleep(1)

    def report(self, successful_accounts: list, failed_accounts: list, stop_pack: str = None, last_task: str = None):
        if stop_pack is None:
            if len(failed_accounts) == 0:
                self.logger.info(f"All accounts processing successfully.")
                sending_result = message_report_to_telegram(f"✅ Merkly || All accounts processing "
                                                            f"successfully: {successful_accounts}")
            else:
                self.logger.warning(f"Some accounts was FAILED: {failed_accounts}")
                sending_result = message_report_to_telegram(f"⚠️ Merkly || Success accounts: {successful_accounts}; "
                                                            f"Failed accounts: {failed_accounts}")
        else:
            if len(failed_accounts) == 0:
                self.logger.info(f"Previous accounts processing successfully.")
                sending_result = message_report_to_telegram(f"✅ Merkly || Success accounts: {successful_accounts}."
                                                            f"Last account: {stop_pack}; last task: {last_task}")
            else:
                self.logger.warning(f"Some accounts was FAILED: {failed_accounts}")
                sending_result = message_report_to_telegram(f"⚠️ Merkly || Success accounts: {successful_accounts}; "
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
        for key in self.accounts:
            skip_pack = False
            if not stop_run:
                try:
                    self.logger.info("*" * 20)
                    if "wallets" in key:
                        private_key = key['wallets']['EVM']['private_key']
                    else:
                        private_key = key['private_key']
                    address = layerzero.utils.get_address_from_private_key(private_key)
                    self.logger.info(f"Processing pack {key['pack']}; Public address: {address}")
                    all_tasks = self.message_generator(private_key, address)
                    for task in all_tasks:
                        self.logger.info(task["action"])

                    work = Workflow()
                    next_account = False
                    last_task = ""

                    for task in all_tasks:
                        if next_account:
                            break
                        if self.event.is_set():
                            stop_run = True
                            self.closing()
                            self.report(successful_accounts, failed_accounts, key["pack"], last_task)
                            self.tabClose.emit(self.tab_name, "Merkly")
                            return -1

                        self.logger.info(task["action"])
                        time.sleep(5)

                        task['logger'] = self.logger
                        task['event'] = self.event
                        for handler in work.handlers:
                            if not stop_run and not skip_pack:
                                result = handler.handle(task)
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
                                        self.tabClose.emit(self.tab_name, "Merkly")
                                        return -1

                                    elif result["code"] in [13, 14, 15]:
                                        failed_accounts.append(key['pack'])
                                        self.logger.warning(result)
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

                    self.logger.info(f"Account {key['pack']} finished work")
                    self.logger.info("Status: SUCCESS\n")
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
