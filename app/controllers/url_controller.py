from flask import url_for, current_app
from flask_sqlalchemy import Pagination
import requests


class UrlController:

    @staticmethod
    def get_next_url(endpoint: str, pagination: Pagination, parameter=None) -> str or None:
        if parameter:
            return url_for(endpoint, **parameter, page=pagination.next_num) if pagination.has_next else None
        else:
            return url_for(endpoint, page=pagination.next_num) if pagination.has_next else None

    @staticmethod
    def get_prev_url(endpoint: str, pagination: Pagination, parameter=None) -> str or None:
        if parameter:
            return url_for(endpoint, **parameter, page=pagination.prev_num) if pagination.has_prev else None
        else:
            return url_for(endpoint, page=pagination.prev_num) if pagination.has_prev else None

    @staticmethod
    def weather_request(city='Minsk') -> tuple:
        data = requests.get(
            f'http://api.openweathermap.org/data/2.5/find?q={city}&type=like&'
            f'APPID={current_app.config["YOUR_ACCESS_KEY"]}&units=metric&lang=ru'
        ).json()

        loc_info = {'region': data['list'][0]['name']}
        weather_info = {'temperature': data['list'][0]['main']['temp']}

        return loc_info, weather_info
