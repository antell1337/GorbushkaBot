from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
import os

storage = MemoryStorage()
load_dotenv()
bot = Bot(token=os.getenv('TG_KEY'))
dp = Dispatcher(bot, storage=storage)

# создание основных переменных bot и dp - создание подключения и от него хранилище для бота
