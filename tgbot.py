import telebot
import main
bot = telebot.TeleBot(token="ТОКЕН")
@bot.message_handler(commands=['start', 'reset'])
@bot.message_handler(content_types = ["text"])
def echo_all(message):
    # message.chat.id - ID чата
    # message.text - текст сообщения
    chat_id=(message.chat.id)
    user_text = message.text
    answer_from_lachuga = main.lachuga(chat_id,user_text)
    bot.reply_to(message, answer_from_lachuga or "Данные не найдены")
def restart(message):
    message.chat.id = []
bot.infinity_polling()
