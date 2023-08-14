# FlowerShop
Телеграм бот для заказа цветов.

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
    - SECRET_KEY - секретный ключ проекта. Получить можно например [здесь](https://djecrety.ir/)
    - TG_BOT_TOKEN - токен телеграм бота. Получить можно у https://t.me/BotFather
 - Запустить бота
```shell
poetry run python namage.py tg_bot
```

Данное описание является стартовым, нужно для старта работы над проектом.  
В последствии будет дополняться и меняться.