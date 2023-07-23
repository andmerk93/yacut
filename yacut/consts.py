from string import ascii_letters, digits

APPROVED_SYMBOLS = ascii_letters + digits
ORIGINAL_LINK_LENGTH = 512
RANDOM_GEN_TRYS = 3
SHORT_LINK_LENGTH = 16
SHORT_LINK_RANDOM_LENGTH = 6
SHORT_LINK_REXEXP = f'[{APPROVED_SYMBOLS}]+'
SHORT_LINK_FUNCTION_NAME = 'link_redirect_view'

WRONG_SHORT_ID = 'Указанный id не найден'
EMPTY_REQUEST_JSON = 'Отсутствует тело запроса'
NO_URL_IN_REQUEST_JSON = '"url" является обязательным полем!'
LONG_URL_ALREADY_EXISTS = 'Имя "{0}" уже занято.'
WRONG_NAME_FOR_SHORT_URL = 'Указано недопустимое имя для короткой ссылки'
