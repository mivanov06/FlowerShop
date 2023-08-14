from enum import IntEnum


class CustomerState(IntEnum):
    START = 1
    AMOUNT_CHOICE = 2
    BOUQUET = 3
    CHOICE_BOUQUET = 4
    PAYMENT = 5
    CONSULTATION = 6
    ADDRESS = 7
    PHONE_NUMBER = 8
    CHECK_INFO = 9
    CREATE_ORDER = 10
