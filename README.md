# gcalendar
Google calendar events collector

**перед запуском:**

создать `.env` файл с переменными окружения в web/gcalendar/ по примеру **.env_example**

_Переменные окружения для подключения к БД и Google calendar API можно указать либо в .env, либо как переменные окружения среды:_

    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY - ID Oauth2 приложения Google cloud platform
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET - Ключ Oauth2 приложения Google cloud platform
    DB_USER - имя пользователя БД
    DB_PASS - пароль пользователя БД
    DB_HOST - хост БД
    DB_PORT - порт БД
    DB_NAME - имя БД

**для запуска проекта вручную, выполнить команды:**

1. `pip install -r requirements.txt`

2. `python manage.py migrate`

3. `python manage.py runserver HOST:PORT`


**для запуска в docker-контейнере:**

1. Установить docker и docker-compose

из коневой директории (gcalendar) выполнить команды:
2. `sudo docker-compose -f _CI/docker-compose.yml build`
3. `sudo docker-compose -f _CI/docker-compose.yml up`

**URL**s:

**/** - основная страница

**admin/** - панель администратора django

