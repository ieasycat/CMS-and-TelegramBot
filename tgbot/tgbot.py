from telebot import TeleBot, types
from config import CONFIG
from telegrambot_controllers import TelegramBotController


def telegram_bot(token):
    bot = TeleBot(token)

    technology = ('Python', 'DevOps', 'Android', 'UI/UX', 'Flutter')
    level = ('Python Middle', 'Python Senior', 'DevOps Middle', 'DevOps Senior',
             'Android Middle', 'Android Senior', 'UI/UX Middle', 'UI/UX Senior',
             'Flutter Middle', 'Flutter Senior')

    @bot.message_handler(commands=['start'])
    @bot.message_handler(func=lambda message: message.text == 'Back')
    def start(message):
        text = 'Please choose a suitable specialty: '

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        key_python = types.InlineKeyboardButton(text='Python', callback_data='python')
        key_devops = types.InlineKeyboardButton(text='DevOps', callback_data='devops')
        key_android = types.InlineKeyboardButton(text='Android', callback_data='android')
        key_ui_ux = types.InlineKeyboardButton(text='UI/UX', callback_data='ui/ux')
        key_flutter = types.InlineKeyboardButton(text='Flutter', callback_data='flutter')

        keyboard.add(key_python, key_devops, key_android, key_ui_ux, key_flutter)

        bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

    @bot.message_handler(func=lambda message: message.text in technology)
    def filter_employee(message):
        text = 'Please select the specialist level: '

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
        key_middle = types.InlineKeyboardButton(text=f'{message.text} Middle', callback_data='middle')
        key_senior = types.InlineKeyboardButton(text=f'{message.text} Senior', callback_data='senior')
        key_start = types.InlineKeyboardButton(text='Back', callback_data='back')
        keyboard.add(key_middle, key_senior, key_start)

        bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

    @bot.message_handler(func=lambda message: message.text in level)
    def handler_text(message):
        res = message.text.split()

        employees_free = TelegramBotController.get_employee(res=res, status='Free')
        employees_busy = TelegramBotController.get_employee(res=res, status='Busy', date=30)

        for employee in employees_free:
            TelegramBotController.send_employee(employee=employee, bot=bot, message=message)

        if employees_busy:
            bot.send_message(message.chat.id, text='These specialists will be released within a month')

            for employee in employees_busy:
                TelegramBotController.send_employee(employee=employee, bot=bot, message=message)

    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    telegram_bot(token=CONFIG.TOKEN)
