import datetime

import phonenumbers

from telegram import Update
from telegram import ReplyKeyboardRemove
from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton

from telegram.ext import CallbackContext
from telegram.ext import ConversationHandler

from src.bot import utils
from src.bot.states import CustomerState


def start_for_customer(update: Update, context: CallbackContext):
    button_names = [
        'День рождения',
        'Свадьба',
        'Другое'
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='К какому событию готовимся? \n'
             'Выберите один из вариантов, либо укажите свой',
        reply_markup=utils.create_tg_keyboard_markup(
            button_names,
            buttons_per_row=2,
        )
    )
    return CustomerState.AMOUNT_CHOICE


def amount_choice(update: Update, context: CallbackContext):
    button_names = [
        '500',
        '1000',
        '5000',
        'не важно'
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='На какую сумму рассчитываете?',
        reply_markup=utils.create_tg_keyboard_markup(
            button_names,
            buttons_per_row=3,
        )
    )
    return CustomerState.BOUQUET


def get_bouquet_flowers(update: Update, context: CallbackContext):
    button_names = [
        'Заказать консультацию',
        'Посмотреть всю коллекцию'
    ]

    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo='https://storage.florist.ru/cdn-cgi/image/format=webp/f/get'
              '/content/bouquet/e5/21/_eaf70d5d55124889c9bb2633eb14/800x800'
              '/6268e7407ce08.jpg',
        caption='Cлучайный букет \n Описание букета \nстоимость',
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Оплата", callback_data='payment')]
            ]
        )
    )

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Хотите что-то более специальное? Подберите другой букет из '
             'нашей коллекции или закажите личную консультацию',
        reply_markup=utils.create_tg_keyboard_markup(
            button_names,
            buttons_per_row=3,
        )
    )
    return CustomerState.CHOICE_BOUQUET


def start_payment(update: Update, context: CallbackContext):
    if update.callback_query.data == 'payment':
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Как вас зовут?'
        )
        return CustomerState.PAYMENT


def choice_bouquet(update: Update, context: CallbackContext):
    if update.message.text == 'Заказать консультацию':
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Укажите номер телефона, и наш флорист перезвонит вам в '
                 'течение 20 минут',
        )
        return CustomerState.CONSULTATION

    return get_bouquet_flowers(update, context)


def get_customer_address(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Введите Ваш адрес',
    )
    return CustomerState.ADDRESS


def get_phone_number(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Введите Ваш номер телефона',
    )
    return CustomerState.PHONE_NUMBER


def get_delivery_time(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Выберите дату и время доставки! '
             'Введите дату в формате: год-месяц-день час',
    )
    return CustomerState.CHECK_INFO


def check_customer_information(update: Update, context: CallbackContext):
    customer = ''
    try:
        parsed_phonenumber = phonenumbers.parse(
            update.message.text,
            'RU'
        )
    except:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Номер телефона был введен неправильно, повторите попытку',
        )
        return CustomerState.PHONE_NUMBER

    if phonenumbers.is_valid_number(parsed_phonenumber):
        customer.phone_number = phonenumbers.format_number(
            parsed_phonenumber,
            phonenumbers.PhoneNumberFormat.E164
        )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Введеный Вами номер телефона не существует. Попробуйте '
                 'ввести через +7',
        )
        return CustomerState.PHONE_NUMBER
    button_names = [
        'Да',
        'Нет'
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Верны ли Ваши данные?\n Адрес: {customer.address} '
             f'Номер телефона: {update.message.text}',
        reply_markup=utils.create_tg_keyboard_markup(
            button_names,
            buttons_per_row=2,
        )
    )
    return CustomerState.CREATE_ORDER


def create_order(update: Update, context: CallbackContext):
    order = ''
    try:
        delivery_time = datetime.datetime.strptime(
            update.message.text,
            '%Y-%m-%d').date()
        order.delivery_time = delivery_time
        order.order_end_date = order.delivery_time + datetime.timedelta(
            days=order
        )
    except:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Попробуйте ещё раз, например 2023-06-15',
        )
        return CustomerState.CREATE_ORDER
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Спасибо за уделенное время. Информация о доставке \n '
             f'Для повторной сессии напишите в чат /start',
    )
    return ConversationHandler.END


def cancel(update, _):
    update.message.reply_text(
        'Спасибо за уделенное Вами время'
        'Если хотите продолжить работу введите команду'
        '/start',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END
