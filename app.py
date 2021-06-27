import logging
from flask import Flask, request
from telegram import Bot, Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Filters, Dispatcher
from utils import get_reply, fetch_news, topics_keyboard
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


TOKEN = "HiddenToken that is used to uniquely identify the bot"

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello!"

@app.route(f'/{TOKEN}', methods = ['GET','POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    dp.process_update(update)
    return "ok"

def start(bot, update):
    """Send a message when the command /start is issued."""
    bot.send_message(chat_id=update.message.chat_id, text='Hi!')

def _help(bot, update):
    help_reply = "This is a help text"
    bot.send_message(chat_id = update.message.chat_id, text = help_reply)

def news(bot, update):
    bot.send_message(chat_id= update.message.chat_id, text = 'Choose a category',
                    reply_markup=ReplyKeyboardMarkup(keyboard=topics_keyboard, one_time_keyboard=True))


def reply_text(bot, update):
    intent, reply = get_reply(update.message.text, update.message.chat_id)
    if intent == "get_news":
        articles = fetch_news(reply)
        for article in articles:
            bot.send_message(chat_id = update.message.chat_id, text = article['link'])
    else:
        bot.send_message(chat_id = update.message.chat_id, text = reply)

def echo_sticker(bot, update):
    bot.send_sticker(chat_id = update.message.chat_id, sticker = update.message.sticker.file_id)

def error(bot, update):
    logger.error("Update '%s' has cause '%s' error", update, update.error)

bot = Bot(TOKEN)
try:
    bot.set_webhook("https://still-beyond-05463.herokuapp.com/" + TOKEN)
except Exception as e:
    print(e)

dp = Dispatcher(bot, None)
dp.add_handler(CommandHandler("start",start))
dp.add_handler(CommandHandler("help",_help))
dp.add_handler(CommandHandler("news", news))
dp.add_handler(MessageHandler(Filters.text, reply_text))
dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))
dp.add_error_handler(error)


if __name__ == '__main__':
    app.run(port = 8443)
