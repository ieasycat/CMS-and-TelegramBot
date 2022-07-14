from telebot import TeleBot, types
from config import CONFIG


def telegram_bot(token):
    bot = TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start(message):
        text = 'Please choose a suitable specialty: '

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key_python = types.InlineKeyboardButton(text='Python', callback_data='python')
        key_devops = types.InlineKeyboardButton(text='DevOps', callback_data='devops')
        key_android = types.InlineKeyboardButton(text='Android', callback_data='android')
        key_ui_ux = types.InlineKeyboardButton(text='UI/UX', callback_data='ui/ux')
        key_flutter = types.InlineKeyboardButton(text='Flutter', callback_data='flutter')

        # key_middle = types.InlineKeyboardButton(text='Middle', callback_data='middle')
        # key_senior = types.InlineKeyboardButton(text='Senior', callback_data='senior')

        keyboard.add(key_python, key_devops, key_android, key_ui_ux, key_flutter)

        bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

    @bot.message_handler(content_types=["text"])
    def handle_text(message):
        text = 'Please select the specialist level: '

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key_middle = types.InlineKeyboardButton(text='Middle', callback_data='middle')
        key_senior = types.InlineKeyboardButton(text='Senior', callback_data='senior')
        keyboard.add(key_middle, key_senior)

        bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    telegram_bot(token=CONFIG.TOKEN)
