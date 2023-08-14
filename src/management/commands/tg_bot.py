from django.conf import settings
from django.core.management.base import BaseCommand

from telegram.ext import Updater

from src.bot.conversations import customer_conversation


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if not settings.TG_BOT_TOKEN:
            print('Не могу запустить команду не задан TG_BOT_TOKEN')

        updater = Updater(settings.TG_BOT_TOKEN, use_context=True)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(customer_conversation, group=-1)

        updater.start_polling(drop_pending_updates=True)
        updater.idle()
