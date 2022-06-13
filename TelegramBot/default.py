import CONFIG
import Classes

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram import types

import sqlite3

owner = int(CONFIG.owner_id)

bot = Bot(token=CONFIG.bot_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

conn = sqlite3.connect('db/shop.db')
cursor = conn.cursor()
table_name = 'games'
cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
    game  STRING  UNIQUE,
    keys  STRING,
    price INTEGER
)""")

bt = Classes.Buttons(conn=conn, cursor=cursor, table_name=table_name)
