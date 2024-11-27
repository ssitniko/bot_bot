from aiogram import Bot, Dispatcher
from decouple import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage



Staff = [489057561,]

token = config('TOKEN')
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)