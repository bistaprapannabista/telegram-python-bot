import os
from dotenv import load_dotenv
import telebot
import requests
import ollama
import py_hot_reload

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")

CURRENCY_TOKEN = os.environ.get("CURRENCY_API_KEY")

def main():

    bot = telebot.TeleBot(BOT_TOKEN)


    @bot.message_handler(commands=["start", "hello"])
    def send_welcome(message):
        bot.reply_to(message, "Hello, how are you doing?")


    @bot.message_handler(func=lambda message: "convert" in message.text.lower())
    def convert_currency(message):
        try:
            inp = message.text.split()
            amount = int(inp[1])
            from_currency = inp[2]
            to_currency = inp[4]
            x = requests.get(
                f"https://api.currencyapi.com/v3/latest?apikey={CURRENCY_TOKEN}&currencies={to_currency}&base_currency={from_currency}"
            )
            data = x.json()
            result = data["data"][to_currency]["value"]
            bot.reply_to(message, f"Today you'll get {result*amount}")
        except:
            bot.reply_to(message,"Please make sure you entered command properly.")



    @bot.message_handler(commands=["help"])
    def send_help(message):
        help_text = "Here are the commands you can use:\n/start - Start the bot\n/hello - Greet the bot\n/help - Display this help message"
        bot.reply_to(message, help_text)


    @bot.message_handler(func=lambda message: "thanks" in message.text.lower())
    def reply_thanks(message):
        bot.reply_to(message, "You're welcome!")

    @bot.message_handler(func=lambda msg: True)
    def response_all(message):
        gre_prompt = f"Solve this GRE question following problem: {message.text} and provide exact answer in first line and in second line detailed explanation of solution process?"
        response = ollama.chat(model='llama3.2', messages=[{
        'role': 'user',
        'content': gre_prompt},])
        bot.reply_to(message, response['message']['content'])

    # @bot.message_handler(func=lambda msg: True)
    # def echo_all(message):
    #     bot.reply_to(message, message.text)


    bot.infinity_polling()

py_hot_reload.run_with_reloader(main)