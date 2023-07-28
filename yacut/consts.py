from re import compile, escape
from string import ascii_letters, digits

APPROVED_SYMBOLS = ascii_letters + digits
ORIGINAL_LINK_LENGTH = 2048
RANDOM_GEN_TRYS = 3
SHORT_LENGTH = 16
SHORT_RANDOM_LENGTH = 6
SHORT_REXEXP = compile(rf'^[{escape(APPROVED_SYMBOLS)}]*$')
SHORT_FUNCTION_NAME = 'link_redirect_view'
