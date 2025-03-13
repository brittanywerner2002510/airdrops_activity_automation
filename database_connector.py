from sqlalchemy import DECIMAL
from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime, Enum, ForeignKey
from sqlalchemy import create_engine, insert, select

with open(".env", "r") as env_file:
    keys = env_file.readlines()


class DatabaseConnector(object):
    CONNECTION_STRING = keys[0].split("=")[1].rstrip()

    meta = MetaData()

    eth_trading = Table(
        "eth_trading", meta,
        Column('id', Integer, primary_key=True),
        Column('pack', String(50)),
        Column('route', Enum('BUY', 'SELL')),
        Column('eth_amount', DECIMAL(26, 16)),
        Column('price', DECIMAL(26, 16)),
        Column('usdt_amount', DECIMAL(26, 16)),
        Column('actions_time', DateTime)
    )

    accounting = Table(
        "accounting", meta,
        Column('id', Integer, primary_key=True),
        Column('pack', String(50)),
        Column('project', String(255)),
        Column('eth_trade_id', Integer, ForeignKey('eth_trading.id', ondelete="CASCADE"), nullable=True),
        Column('route', Enum('WITHDRAW', 'DEPOSIT')),
        Column('coin', String(50)),
        Column('amount', DECIMAL(26, 16)),
        Column('actions_time', DateTime)
    )

    def __init__(self):
        self.engine = create_engine(self.CONNECTION_STRING, pool_pre_ping=True)
        self.meta.bind = self.engine
        self.meta.create_all(self.engine)
        self.db_match = {'accounting': self.accounting, 'eth_trading': self.eth_trading}

    def insert_data(self, table_name: str, data: dict):
        with self.engine.connect() as conn:
            conn.execute(insert(self.db_match[table_name]), data)
            conn.commit()

    def select_data_from_accounting(self, project: str = None):
        conn = self.engine.connect()
        if project is None:
            result = conn.execute(select(self.accounting)).fetchall()
        else:
            result = conn.execute(select(self.accounting)
                                  .where(self.accounting.c.project == project)).fetchall()
        if result:
            return result

    def select_eth_trade_id(self, actions_time):
        conn = self.engine.connect()
        result = conn.execute(select(self.eth_trading.c.id)
                              .where(self.eth_trading.c.actions_time == actions_time)).first()
        if result is not None:
            return int(result[0])
