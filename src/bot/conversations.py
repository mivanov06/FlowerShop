from telegram.ext import ConversationHandler, CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

from src.bot.states import CustomerState
from src.bot import handlers

customer_conversation = ConversationHandler(
    entry_points=[
        CommandHandler(
            'start',
            handlers.start_for_customer
        ),
        MessageHandler(
            Filters.text('Стартовое меню'),
            handlers.start_for_customer
        )
    ],
    states={
        CustomerState.AMOUNT_CHOICE: [
            MessageHandler(
                Filters.text([
                    'День рождения',
                    'На свадьбу',
                    'На свидание',
                    'Другое'
                ]),
                handlers.amount_choice,
                pass_user_data=True,
            ),
        ],
        CustomerState.BOUQUET: [
            MessageHandler(
                Filters.text([
                    '500',
                    '1000',
                    '5000',
                    'не важно'
                ]),
                handlers.get_bouquet_flowers,
                pass_user_data=True,
            ),
        ],
        CustomerState.CHOICE_BOUQUET: [
            CallbackQueryHandler(handlers.start_payment),
            MessageHandler(
                Filters.text([
                    'Заказать консультацию',
                    'Посмотреть всю коллекцию',
                ]),
                handlers.choice_bouquet,
                pass_user_data=True,
            ),
        ],
        CustomerState.PAYMENT: [
            MessageHandler(
                Filters.text,
                handlers.get_customer_address,
                pass_user_data=True,
            ),
        ],

        CustomerState.ADDRESS: [
            MessageHandler(
                Filters.text,
                handlers.get_phone_number,
                pass_user_data=True,
            ),
        ],
        CustomerState.PHONE_NUMBER: [
            MessageHandler(
                Filters.text,
                handlers.get_delivery_time,
                pass_user_data=True,
            ),
        ],
        CustomerState.CHECK_INFO: [
            MessageHandler(
                Filters.text,
                handlers.check_customer_information,
                pass_user_data=True,
            ),
        ],
        CustomerState.CREATE_ORDER: [
            MessageHandler(
                Filters.text(['Да', 'Нет']),
                handlers.create_order,
                pass_user_data=True,
            ),
        ],
    },
    fallbacks=[
        CommandHandler('cancel', handlers.cancel),
        MessageHandler(Filters.text('отмена'), handlers.cancel)
    ]
)
