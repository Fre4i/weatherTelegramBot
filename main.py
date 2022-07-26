import telebot
from dotenv import load_dotenv, find_dotenv
from pprint import pprint
import requests

import os

load_dotenv(find_dotenv())


# ---Функционал---
# 1. /start /help - инструкция по боту
# 2. /addtime - добавление времени напоминания погоды
# 3. /deltime - удаление времени напоминания погоды
# 4. /addtown - добавление города
# 4. /deltown - үдаление города
# 4. /options - заход в настройки бота
# 5.    /enablelocalwarning - включение предупреждения о плохой погоде за 2 часа
# 6.    /enablehourly - включение почасового прогноза
# 7.    /enabletomorrowweather - включение завтрашней погоды (по умолчанию 20:00)

def telegram(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.chat.id, 'Привет!')

    # @bot.message_handler(commands=['help'])
    # def help(message):
    #     pass
    #
    # @bot.message_handler(commands=['addtime'])
    # def add_time(message):
    #     pass
    #
    # @bot.message_handler(commands=['deltime'])
    # def del_time(message):
    #     pass
    #
    # @bot.message_handler(commands=['addtown'])
    # def add_town(message):
    #     pass
    #
    # @bot.message_handler(commands=['deltown'])
    # def del_town(message):
    #     pass
    #
    # @bot.message_handler(commands=['options'])
    # def options(message):
    #     pass
    #
    # @bot.message_handler(commands=['enablelocalwarning'])
    # def enable_local_warning(message):
    #     pass
    #
    # @bot.message_handler(commands=['enablehourly'])
    # def enable_hourly(message):
    #     pass
    #
    # @bot.message_handler(commands=['enabletomorrowweather'])
    # def enable_hourly(message):
    #     pass
    bot.polling()

def open_weather(city):
    open_weather_api = os.getenv('OPENWEATHER_TOKEN')
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_api}'
    response = requests.get(url=url)
    data = response.json()
    pprint(data)


def main():
    telegram(os.getenv('TELEGRAM_TOKEN'))
    # open_weather('Саратов')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
