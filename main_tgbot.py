import requests
import datetime
from conf import tg_token, token_weather
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

# содаем объект бота и передаем в него токен бота
bot = Bot(token=tg_token)
#создаем объект диспетчера и передаем в него бота
dp = Dispatcher(bot)

# функция ответа на команду start
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Напиши название города, а я пришлю тебе сводку по погоде!")

#функция вывода погоды
@dp.message_handler()
async def get_weather(message: types.Message):
    # в блоке try делаем get запрос, получаем и обрабатываем данные

    try:
        # r хранит запрос
        r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={token_weather}&units=metric")

        # data хранит ответ от сайта в формате json
        data = r.json()

        # словарь из состояния погоды и эмоджи к определенной погоде
        code_smile = {
            "Clear": "Ясно \U00002600",
            "Clouds": "Облачно \U00002601",
            "Rain": "Дождь \U00002614",
            "Drizzle": "Дождь \U00002614",
            "Thunderstorm": "Гроза \U000026A1",
            "Snow": "Снег \U0001F328",
            "Mist": "Туман \U0001F32B"
        }

        weather_description = data["weather"][0]["main"]
        # если погоода совпадет со значением из словаря, то забираем это значение
        if weather_description in code_smile:
            wd = code_smile[weather_description]
        else:
            wd = "Лучше тебе самому посмотреть, там что-то страшное"

        # получаем название города
        city = data["name"]
        # получаем температуру из блока main, обращаясь к ключу temp
        cur_weather = data["main"]["temp"]
        # аналогично температуре получаем остальные показатели (влажность, давление, ветер)
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        # т.к. время рассвета и заката передается в формате unix timestemp подключим модуль datetime для удобного вывода
        sunrise_timestemp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestemp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        # для получения продолжительности стветового дня вычтем из времени заката время рассвета
        length_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nСкорость ветра: {wind} м/с\n"
              f"Восход солнца: {sunrise_timestemp}\nЗакат солнца: {sunset_timestemp}\n"
              f"Продолжительность дня: {length_day}")

    # except выводит сообщение об обшибке, если такая возникнет
    except:
        await message.reply(f"\U00002620 Я не смог найти такой город \U00002620"
                            f"\nПопробуй написать название на анлийском.\nУдостоверься, что написал его правильно.")


if __name__ == '__main__':
    executor.start_polling(dp)

