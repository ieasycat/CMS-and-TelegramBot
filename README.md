# CMS and TelegramBot

This is a CMS system for a company that allows you to track the status of employees. Main fitches:
1. Telegram bot, which displays a list of all available employees at the request of the client.
2. API for interaction between telegram bot and Android application.
Only registered users have access. The code is covered with tests. It is also ready for deployment on Heroku and containerized for Docker.

CMS stack: Flask, pyTelegramBotAPI, SQLAlchemy, PyTest, PostgresSQL


command for docker: docker-compose up -d --build
