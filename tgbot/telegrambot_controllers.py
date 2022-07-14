import requests
from config import CONFIG


class TelegramBotController:

    @staticmethod
    def send_employee(employee, bot, message):
        text = f"Level: {employee['programmer_level']}, Nickname: {employee['nickname']},\n" \
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
