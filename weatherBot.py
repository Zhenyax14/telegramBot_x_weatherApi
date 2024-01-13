import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Fill with your Telegram Bot API token
TOKEN = 'Your telegram token'
# Fill with you API OpenWeatherMap
API_KEY = 'Your WeatherApi token'


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hello! Please, send the location to get the weather')


def get_location(update: Update, context: CallbackContext):
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude

    # Вызываем функцию для запроса погоды
    get_weather(update, latitude, longitude)


def get_weather(update: Update, latitude, longitude):
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={API_KEY}&units=metric&lang=en'
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        city = weather_data['name']

        message = f'Current weather in {city}: {description}. Temperature is: {temperature}°C.'
        update.message.reply_text(message)
    else:
        update.message.reply_text('An error has occured.')


def main():
    updater = Updater(TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(MessageHandler(Filters.location, get_location))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()