import datetime

import requests

from database_connector import DatabaseConnector


def message_report_to_telegram(message):
    counter = 0
    while counter < 3:
        with open(".env", "r") as file:
            keys = file.readlines()
        api_token = keys[1].split("=")[1].rstrip()
        chat_id = keys[2].split("=")[1].rstrip()
        url = f"https://api.telegram.org/bot{api_token}"
        method = url + "/sendMessage"
        response = requests.post(method, data={
            "chat_id": int(chat_id),
            "text": message,
            "protect_content": False
        })
        if response.status_code != 200:
            counter += 1
        else:
            return response.json()
    return {"code": -1, "msg": "Can't send message."}


def insert_dispatcher(data_for_insert: dict, pack):
    db = DatabaseConnector()
    if data_for_insert['buy_action'] is not None:
        data = data_for_insert['buy_action']
        data['pack'] = pack
        db.insert_data('eth_trading', data)

    if data_for_insert['sell_action'] is not None:
        data = data_for_insert['sell_action']
        data['pack'] = pack
        db.insert_data('eth_trading', data)

    if data_for_insert['withdraw_action'] is not None:
        data = data_for_insert['withdraw_action']
        data['pack'] = pack
        if data_for_insert['buy_action'] is not None:
            actions_time = datetime.datetime.strftime(data_for_insert['buy_action']['actions_time'],
                                                      "%Y-%m-%d %H:%M:%S")
            eth_trade_id = db.select_eth_trade_id(actions_time)
            data['eth_trade_id'] = eth_trade_id
        db.insert_data('accounting', data)

    if data_for_insert['deposit_action'] is not None:
        data = data_for_insert['deposit_action']
        data['pack'] = pack
        if data_for_insert['sell_action'] is not None:
            actions_time = datetime.datetime.strftime(data_for_insert['sell_action']['actions_time'],
                                                      "%Y-%m-%d %H:%M:%S")
            eth_trade_id = db.select_eth_trade_id(actions_time)
            data['eth_trade_id'] = eth_trade_id
        db.insert_data('accounting', data)
