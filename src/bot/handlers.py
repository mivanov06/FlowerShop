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

from src.models import Bouquet, Order, Consultation, Client


def start_for_customer(update: Update, context: CallbackContext):
    button_names = [
        'День рождения',
        'На свадьбу',
        'На свидание',
        'Другое'
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='К какому событию готовимся? \n'
             'Выберите один из вариантов, либо укажите свой',
        reply_markup=utils.create_tg_keyboard_markup(
            button_names,
            buttons_per_row=3,
        )
    )
    return CustomerState.AMOUNT_CHOICE


def amount_choice(update: Update, context: CallbackContext):
    user_data = context.user_data
    user_data['event'] = update.message.text
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
    user_data = context.user_data
    user_data['amount'] = update.message.text

    if user_data['amount'] == 'не важно':
        user_data['amount'] = 1000000

    if user_data['event'] == 'Другое':
        bouquets = Bouquet.objects.filter(
            price__lte=user_data['amount']
            )

    if update.message.text == 'Посмотреть всю коллекцию':
        bouquets = Bouquet.objects.all()

    else:
        bouquets = Bouquet.objects.filter(
            events__name=user_data['event'],
            price__lte=user_data['amount']
            )

    if not bouquets:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Нет подходящего букета :('
        )

    for bouquet in bouquets:
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=bouquet.image,
            caption=f'Описание:\n{bouquet.description}\n\n'
            f'{bouquet.compound}\n\nСтоимость:\n{bouquet.price}',
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Оплата",
                                          callback_data=f'payment{bouquet.id}')]
                ]
            )
        )

    button_names = [
        'Заказать консультацию',
        'Посмотреть всю коллекцию'
    ]

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
    if update.callback_query.data.startswith('payment'):
        user_data = context.user_data
        user_data['bouquet_id'] = update.callback_query.data[7:]
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


def process_consultation_choice(update: Update, context: CallbackContext):
    user_data = context.user_data
    user_data['name'] = update.message.from_user.username
    user_data['phonenumber'] = update.message.text
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Спасибо, ваша заявка на консультацию принята, '
             'мы скоро свяжемся с вами',
    )
    client, _ = Client.objects.get_or_create(
        name=user_data['name'],
        phonenumber=user_data['phonenumber']
    )
    Consultation.objects.create(client=client)

    return ConversationHandler.END


def get_customer_address(update: Update, context: CallbackContext):
    user_data = context.user_data
    user_data['name'] = update.message.text
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Введите Ваш адрес',
    )
    return CustomerState.ADDRESS


def get_phone_number(update: Update, context: CallbackContext):
    user_data = context.user_data
    user_data['address'] = update.message.text
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Введите Ваш номер телефона',
    )
    return CustomerState.PHONE_NUMBER


def get_delivery_date(update: Update, context: CallbackContext):
    user_data = context.user_data
    user_data['phonenumber'] = update.message.text

    try:
        parsed_phonenumber = phonenumbers.parse(
            user_data['phonenumber'],
            'RU'
        )
    except:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Номер телефона был введен неправильно, повторите попытку',
        )
        return CustomerState.PHONE_NUMBER

    if phonenumbers.is_valid_number(parsed_phonenumber):
        user_data['phonenumber'] = phonenumbers.format_number(
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

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Введите дату доставки в формате: год-месяц-день',
    )
    return CustomerState.DELIVERY_DATE


def get_delivery_time(update: Update, context: CallbackContext):
    user_data = context.user_data
    user_data['delivery_date'] = update.message.text

    try:
        user_data['delivery_date'] = datetime.datetime.strptime(
            user_data['delivery_date'],
            '%Y-%m-%d').date()
    except:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Попробуйте ещё раз, например 2023-06-15',
        )
        return CustomerState.DELIVERY_DATE

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Выберите время доставки:\n'
             '1. Как можно скорее\n'
             '2. С 10:00 до 12:00\n'
             '3. С 12:00 до 14:00\n'
             '4. С 14:00 до 16:00\n'
             '5. С 16:00 до 18:00\n'
             '6. С 18:00 до 20:00'
             )
    return CustomerState.CHECK_INFO


def check_customer_information(update: Update, context: CallbackContext):
    user_data = context.user_data
    user_data['delivery_time'] = update.message.text

    if int(user_data['delivery_time']) not in (1, 2, 3, 4, 5, 6):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Выберите вариант от 1 до 6',
        )
        return CustomerState.CHECK_INFO

    button_names = [
        'Да',
        'Нет'
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Верны ли Ваши данные?\n Адрес: {user_data["address"]}\n'
             f'Номер телефона: {user_data["phonenumber"]}',
        reply_markup=utils.create_tg_keyboard_markup(
            button_names,
            buttons_per_row=2,
        )
    )
    return CustomerState.CREATE_ORDER


def create_order(update: Update, context: CallbackContext):
    user_data = context.user_data

    if update.message.text == 'Нет':
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Введите Ваш адрес',
            )
        return CustomerState.ADDRESS

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Спасибо за уделенное время. Информация о доставке \n '
             'Для повторной сессии напишите в чат /start',
    )
    bouquet = Bouquet.objects.get(pk=user_data['bouquet_id'])
    client, _ = Client.objects.get_or_create(
        name=user_data['name'],
        phonenumber=user_data['phonenumber']
    )
    Order.objects.create(bouquet=bouquet,
                         price=bouquet.price,
                         client=client,
                         delivery_date=user_data['delivery_date'],
                         address=user_data['address'],
                         delivery_slot=int(user_data['delivery_time']),
                         )
    return ConversationHandler.END


def cancel(update, _):
    update.message.reply_text(
        'Спасибо за уделенное Вами время\n'
        'Если хотите продолжить работу введите команду\n'
        '/start',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END
