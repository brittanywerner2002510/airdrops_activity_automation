import datetime
import json
import os
import random
import shutil
import sys
import time
from pathlib import Path
from threading import Event

from PySide6.QtCore import QObject, Slot, Signal, QTimer, QThread
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from web3 import Web3, HTTPProvider

from interface import Aptos, LayerZero, Merkly


class Worker(QObject):
    updateGas = Signal(str)
    finished = Signal()
    w3 = Web3(HTTPProvider("https://rpc.ankr.com/eth"))

    def __init__(self):
        super().__init__()

    @Slot(int)
    def update_gas(self):
        while True:
            current_gas_wei = self.w3.eth.gas_price
            current_gas = int(self.w3.from_wei(current_gas_wei, 'gwei'))
            self.updateGas.emit(str(current_gas))
            time.sleep(15)


class Launcher(QObject):
    project_instances = {
        "Layer Zero": {
            "count": 0,
            "adapter": LayerZero
        },
        "Aptos": {
            "count": 0,
            "adapter": Aptos
        },
        "Merkly": {
            "count": 0,
            "adapter": Merkly
        }
    }

    setDatetime = Signal(str)
    addAccount = Signal(list, QObject, str)
    updateGas = Signal(str)
    addTab = Signal(str, str, str)
    log = Signal(str)
    timeValidator = Signal(bool)
    tabFinish = Signal(str)
    tabClose = Signal(str, str)
    showMessageBox = Signal(str, str)
    loadConfigs = Signal(str, list)

    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.checkbox_list = {}
        self.file_name = str()
        self.timer.timeout.connect(lambda: self.set_time())
        self.timer.start(1000)
        self.accounts = {}
        self.active_accounts = {}

        self.worker = Worker()
        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.worker.update_gas)
        self.worker.updateGas.connect(self.updateGas)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)
        self.worker_thread.start()

        self.tab_name = ""
        self.tab_cache = dict()
        self.project_cache = dict()
        self.tab_names = []

    @Slot(str, str)
    def file_handler(self, path_to_file: str, tab_name: str):
        if os.name == "nt":
            path_to_file = path_to_file.lstrip("file:///")
        else:
            path_to_file = f'/{path_to_file.lstrip("file://")}'

        with open(path_to_file, "r") as accounts_file:
            accounts_info = json.load(accounts_file)
        self.__show_accounts_toggle(accounts_info, tab_name)

    def __show_accounts_toggle(self, accounts: list, tab_name: str):
        list_model = self.tab_cache[tab_name].findChild(QObject, f"list_model_{tab_name}")
        packs = []
        for account in accounts:
            pack = account['pack']
            self.accounts[pack] = account
            packs.append(pack)
        self.addAccount.emit(packs, list_model, tab_name)

    def set_time(self):
        current_datetime = datetime.datetime.now()
        format_datetime = current_datetime.strftime("%d.%m.%Y %H:%M:%S")
        self.setDatetime.emit(format_datetime)

    @Slot(list, bool)
    def get_active_accounts(self, accounts: list, shuffle_wallets: bool):
        self.active_accounts.clear()
        self.active_accounts = [self.accounts[account] for account in accounts]
        if shuffle_wallets:
            random.shuffle(self.active_accounts)

    @Slot(str, str)
    def add_project_on_tab_bar(self, project_name: str, config_name: str):
        if self.project_instances[project_name]['count'] < 5:
            for i in range(1, 6):
                tab_name = f"{project_name} {i}"
                if tab_name not in self.tab_names:
                    self.tab_name = tab_name
                    self.tab_names.append(self.tab_name)
                    self.addTab.emit(self.tab_name, project_name, config_name)
                    self.project_instances[project_name]['count'] += 1
                    break

    @Slot(QObject)
    def save_tab(self, new_tab_object: QObject):
        self.tab_cache[self.tab_name] = new_tab_object

    @Slot(str, str)
    def time_validator(self, time_from: str, time_to: str):
        time_from = time_from.split(":")
        time_to = time_to.split(":")

        time_from_hours = int(time_from[0])
        time_from_minutes = int(time_from[1])
        time_to_hours = int(time_to[0])
        time_to_minutes = int(time_to[1])

        if time_to_hours < time_from_hours:
            self.timeValidator.emit(False)
        elif time_to_hours == time_from_hours:
            if time_to_minutes < time_from_minutes:
                self.timeValidator.emit(False)
            else:
                self.timeValidator.emit(True)
        else:
            self.timeValidator.emit(True)

    def save_bridge(self, tab_name: str, bridge: Aptos | LayerZero):
        self.project_cache[tab_name] = bridge

    @Slot(dict, str, str)
    def run_project(self, params: dict, project_name: str, tab_name: str):
        output_field = self.tab_cache[tab_name].findChild(QObject, tab_name)
        accounts = self.active_accounts.copy()
        event = Event()
        adapter = self.project_instances[project_name]["adapter"](accounts, params, output_field, tab_name, event)
        if len(accounts) == 0:
            adapter.logger.error("You haven't selected any accounts!")
            return -1
        self.save_bridge(tab_name, adapter)
        adapter.tabFinish.connect(self.tabFinish)
        adapter.tabClose.connect(self.tabClose)
        adapter.run()

    @Slot(str, str)
    def remove_tab(self, project_name: str, tab_name: str):
        self.project_instances[project_name]["count"] -= 1
        self.tab_names.remove(tab_name)
        self.tab_cache.pop(tab_name)

    @Slot(str, str)
    def close_tab(self, tab_name: str, project_name: str):
        bridge = self.project_cache.get(tab_name, None)
        if bridge is not None and bridge.in_work:
            self.showMessageBox.emit(tab_name, project_name)
        else:
            self.tabClose.emit(tab_name, project_name)

    @Slot(str)
    def stop_tab(self, tab_name: str):
        self.project_cache[tab_name].logger.warning("Get signal to stop work and close tab. The tab will be "
                                                    "safely closed after the current task is completed")
        self.project_cache[tab_name].event.set()

    @Slot(str)
    def load_configs(self, project_name: str):
        if os.path.exists(f"settings/{project_name}") and len(os.listdir(f"settings/{project_name}")) > 0:
            configs = os.listdir(f"settings/{project_name}")
            self.loadConfigs.emit(project_name, configs)
        else:
            self.loadConfigs.emit(project_name, [])

    @Slot(str, str, str)
    def save_config(self, project_name: str, source_config_name: str, config_name: str):
        src_path = f"settings/{project_name}/{source_config_name}"
        destination_path = f"settings/{project_name}/{config_name}"
        shutil.copy(src_path, destination_path)


def run():
    app = QGuiApplication(sys.argv)
    app.setOrganizationName("None")
    app.setOrganizationDomain("None")
    app.setApplicationName("AirDrop Activity Automation")
    engine = QQmlApplicationEngine()
    launcher = Launcher()
    engine.rootContext().setContextProperty("backend", launcher)
    qml_file = Path(__file__).resolve().parent / "qml/main.qml"
    engine.load(qml_file)
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())


if __name__ == "__main__":
    run()
