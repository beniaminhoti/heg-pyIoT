import os
import telebot
from datetime import datetime
from dotenv import load_dotenv
from weather import getWeather


def telegram_bot(bot):
    @bot.message_handler(commands=['Hello', 'hello', 'Hi', 'hi', 'Hey', 'hey', 'Yo', 'yo', 'start', 'Start'])
    def send_welcome(message):
        name = message.from_user.first_name
        bot.reply_to(message, f"Howdy, {name}. How are you doing?")

    @bot.message_handler(commands=['id', 'ID', 'Id', 'iD', 'chat_id', 'Chat_id', 'Chat_Id', 'chat_Id'])
    def send_chat_id(message):
        chat_id = message.chat.id
        print(chat_id)
        bot.reply_to(message, f"Your chat id is: {chat_id}")

    @bot.message_handler(commands=['time', 'Time'])
    def send_time(message):
        now = datetime.now()
        date_time = now.strftime("%d.%m.%Y, %H:%M:%S")
        bot.reply_to(message, date_time)

    @bot.message_handler(commands=['weather', 'Weather'])
    def send_welcome(message):
        txt = message.text
        location = txt[9:]  # remove '/weather '
        temperature = getWeather(location)
        # bot.reply_to(message, "Hello "+name+" the weather in the city: "+location+" is "+str(temperature)+"°C")
        bot.reply_to(message, temperature)

    # Command that sends time and weather in a tuple
    @bot.message_handler(commands=['time_weather', 'Time_weather'])
    def send_time_weather(message):
        now = datetime.now()
        date_time = now.strftime("%d.%m.%Y, %H:%M:%S")
        txt = message.text
        location = txt[14:]
        temperature = getWeather(location)
        bot.reply_to(message, (date_time, temperature))

    # @bot.message_handler(func=lambda msg: True)
    # def echo_all(message):
    #     bot.reply_to(message, message.text)


def send_notification(bot, chat_id, message):
    bot.send_message(chat_id, message)

################################################################
# Main
def main():
    load_dotenv('.env')



    # Telegram Bot API key
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    bot = telebot.TeleBot(BOT_TOKEN)

    # Telegram chat ID
    CHAT_ID = os.getenv('CHAT_ID')  

    send_notification(bot, CHAT_ID, "Bot started")
    telegram_bot(bot)

    bot.infinity_polling()
################################################################

if __name__ == "__main__":
    main()
