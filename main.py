import time

import telebot
from dotenv import load_dotenv, find_dotenv
from pprint import pprint
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By

from PIL import Image

import os

load_dotenv(find_dotenv())

before_info = {
    'Город': '',
    'Температура': '',
    'Ощущается как': '',
    'Осдаки': '',  # ясно, пасмурно
    'Ветер': '',
    'Влажность': '',
    'Давление': '',
    'В ближайшее время': '',
    'Восход': '',
    'Закат': ''
}


def parse_info(city):
    before_info['Город'] = city

    driver = webdriver.Chrome()

    url = f'https://yandex.ru/pogoda/{city}/'
    driver.get(url)
    time.sleep(5)

    # coords = driver.current_url
    # coords = coords.replace(url[:-1], '')
    # coords = coords.replace('?', '')
    # coords = coords.split('&')
    # before_info['lat'] = coords[0]
    # before_info['lon'] = coords[1]

    # driver.save_screenshot('test.png')

    src = driver.page_source

    driver.close()
    driver.quit()

    soup = bs(src, 'lxml')

    temp = soup.find('span', class_='temp__value temp__value_with-unit').text + '°'
    before_info['Температура'] = temp

    temp_feel = soup.find('div', class_='term term_orient_h fact__feels-like')
    temp_feel = temp_feel.find('span', class_='temp__value temp__value_with-unit').text + '°'
    before_info['Ощущается как'] = temp_feel

    downfall = soup.find('div', class_='link__condition day-anchor i-bem').text
    before_info['Осдаки'] = downfall

    wind_speed = soup.find('span', class_='wind-speed').text + ' м/с'
    wind_direction = soup.find('abbr', class_='icon-abbr').text
    before_info['Ветер'] = wind_speed + ', ' + wind_direction

    humidity = soup.find('div', class_='term term_orient_v fact__humidity')
    humidity = humidity.find('div', class_='term__value').text
    before_info['Влажность'] = humidity

    pressure = soup.find('div', class_='term term_orient_v fact__pressure')
    pressure = pressure.find('div', class_='term__value').text
    before_info['Давление'] = pressure

    next_two_hours = soup.find('p', class_='maps-widget-fact__title').text
    before_info['В ближайшее время'] = next_two_hours.replace('\xa0', ' ').lower()

    sunrise = soup.find('div',
                        class_='sun-card__sunrise-sunset-info sun-card__sunrise-sunset-info_value_rise-time').text
    before_info['Восход'] = sunrise.split('Восход')[1]

    sunset = soup.find('div', class_='sun-card__sunrise-sunset-info sun-card__sunrise-sunset-info_value_set-time').text
    before_info['Закат'] = sunset.split('Закат')[1]

    return before_info


def save_screen_weather(city):
    url = f'https://yandex.ru/pogoda/{city}/maps/nowcast?via=mmapwb&le_Lightning=1'

    driver = webdriver.Chrome()
    driver.set_window_position(0, 0)
    driver.set_window_size(1024, 768)

    driver.get(url)
    time.sleep(5)

    # gif
    frames = []

    for i in range(14, 24):
        driver.save_screenshot(f'weather_map_screens/next_two_hours_{i}.png')

        # crop im
        im = Image.open(f'weather_map_screens/next_two_hours_{i}.png')
        # im_crop = im.crop((1600, 300, 3850, 1850))
        # im_crop.save(f'next_two_hours_{i}.png')
        frames.append(im)

        time.sleep(2)
        content = driver.find_element(By.XPATH, f"/html/body/div[3]/div[2]/div[7]/div/div[2]/div[2]/div/div[{i}]")
        content.click()

    frames[0].save(
        'next_90_min.gif',
        save_all=True,
        append_images=frames[1:],
        optimize=True,
        duration=1000,
        loop=0,
        quality=50
    )
    driver.close()
    driver.quit()




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
        ChatID = message.chat.id
        bot.send_message(ChatID, 'Привет!')

    @bot.message_handler(content_types=['text'])
    def weather(message):
        ChatID = message.chat.id
        # after_info = parse_info(city=message.text)

        # mes = ''
        # for key in after_info.keys():
        #     mes += key
        #     mes += ': ' + after_info.get(key) + '\n'

        # bot.send_message(ChatID, mes)
        # save_screen_weather(before_info['Город'])
        save_screen_weather('moscow')
        with open('next_90_min.gif', 'rb') as file:
            bot.send_animation(ChatID, file, caption="mes")

    @bot.message_handler(commands=['help'])
    def help(message):
        pass

    @bot.message_handler(commands=['addtime'])
    def add_time(message):
        pass

    @bot.message_handler(commands=['deltime'])
    def del_time(message):
        pass

    @bot.message_handler(commands=['addtown'])
    def add_town(message):
        pass

    @bot.message_handler(commands=['deltown'])
    def del_town(message):
        pass

    @bot.message_handler(commands=['options'])
    def options(message):
        pass

    @bot.message_handler(commands=['enablelocalwarning'])
    def enable_local_warning(message):
        pass

    @bot.message_handler(commands=['enablehourly'])
    def enable_hourly(message):
        pass

    @bot.message_handler(commands=['enabletomorrowweather'])
    def enable_hourly(message):
        pass

    bot.polling(none_stop=True)


def open_weather(city):
    open_weather_api = os.getenv('OPENWEATHER_TOKEN')
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_api}'
    response = requests.get(url=url)
    data = response.json()
    pprint(data)


def yandex_parse(city):
    global driver
    try:

        # options = selenium.webdriver.ie.options.Options()
        # options.add_argument("--headless")
        # options.add_argument("window-size=100, 100")

        driver = webdriver.Chrome()

        driver.get(f'https://yandex.ru/pogoda/{city}/')
        time.sleep(5)
        # driver.save_screenshot('test.png')

        src = driver.page_source

        soup = bs(src, 'lxml')

        # with open('index_selenium.html', 'w', encoding="utf-8") as file:
        #     file.write(str(driver.page_source))

        print(soup.find(name='span', class_='temp__value temp__value_with-unit').text)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def main():
    # yandex_parse('moscow')
    telegram(os.getenv('TELEGRAM_TOKEN'))


# telegram(os.getenv('TELEGRAM_TOKEN'))
# open_weather('Саратов')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
