# FlowerShop
Сайт и Телеграм бот цветочного магазина.

## Как запустить
 - установить [poetry](https://python-poetry.org/docs/#installation)
 - скачать код с github
```shell
https://github.com/Stranix/FlowerShop.git
```
 - установить зависимости проекта
```shell
poetry install
```
 - Задать обязательные переменные окружения
    - `SECRET_KEY` - секретный ключ проекта. Получить можно например [здесь](https://djecrety.ir/)
 - Запустить сайт в `dev` режиме
   - Установить переменную окружения `DEBUG=True`.
   - Запустить:
   ```shell
   poetry run python manage.py runserver
   ```
## Запуск бота
Обязательно задать переменную окружения `TG_BOT_TOKEN`.  
`TG_BOT_TOKEN` - токен телеграм бота. Получить можно у https://t.me/BotFather
```shell
poetry run python namage.py tg_bot
```

Данное описание является стартовым, нужно для старта работы над проектом.  
В последствии будет дополняться и меняться.