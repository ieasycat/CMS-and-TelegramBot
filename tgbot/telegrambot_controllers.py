import requests
from config import CONFIG
from app.models.dbmodels import Employee
from telebot import TeleBot
from telebot.types import Message


class TelegramBotController:

    @staticmethod
    def send_employee(employee: Employee, bot: TeleBot, message: Message):
        text = f"Nickname: {employee['nickname']},\n" \
               f"Level: {employee['programmer_level']},\n" \
               f"CV: {employee['cv']}"
        return bot.send_message(message.chat.id, text=text)

    @staticmethod
    def get_employee(res: list, status: str, date: int = None):
        return requests.get(CONFIG.URL, json={
            'main_technology': res[0],
            'programmer_level': res[1],
            'status': status,
            'date': date
        }, headers=CONFIG.HEADERS).json()['employees']
