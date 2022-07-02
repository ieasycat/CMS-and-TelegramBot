from app import app
from flask import url_for
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
            f'http://api.weatherstack.com//current?access_key={app.config["YOUR_ACCESS_KEY"]}&query={city}').json()

        loc_info = {'region': data['location']['region'], 'time': data['location']['localtime'].split()[1]}
        weather_info = {'temperature': data['current']['temperature'],
                        'weather_icons': data['current']['weather_icons'][0]}

        return loc_info, weather_info
