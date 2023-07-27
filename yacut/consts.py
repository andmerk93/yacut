from re import compile
from string import ascii_letters, digits

APPROVED_SYMBOLS = ascii_letters + digits
ORIGINAL_LINK_LENGTH = 2048
RANDOM_GEN_TRYS = 3
SHORT_LINK_LENGTH = 16
SHORT_LINK_RANDOM_LENGTH = 6
SHORT_LINK_REXEXP = compile(r'(?a)[\w]+')
SHORT_LINK_FUNCTION_NAME = 'link_redirect_view'
