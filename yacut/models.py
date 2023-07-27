from datetime import datetime
from random import choices
from re import fullmatch

from . import db
from .consts import (
    APPROVED_SYMBOLS,
    ORIGINAL_LINK_LENGTH,
    RANDOM_GEN_TRYS,
    SHORT_LENGTH,
    SHORT_RANDOM_LENGTH,
    SHORT_REXEXP,
)
from .error_handlers import (
    GeneratedShortException,
    LongURLIsBadException,
    ShortIsBadException,
    ShortIsExistsException
)


GENERATING_IS_FALLED = 'Генерация имени не удалась'
SHORT_DOESNT_SUITE_REGEXP = 'Не соответствует разрешенным символам'
SHORT_IS_EXISTS = 'Такое имя уже существует'
WRONG_LENGTH_IN_SHORT = 'Не соответствует разрешенной длине'
ORIGINAL_LINK_IS_EXISTS = 'Такая ссылка уже есть в базе'
ORIGINAL_LINK_IS_BIG = 'Ссылка первышает допустимый размер'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(
        db.String(ORIGINAL_LINK_LENGTH), unique=True, nullable=False
    )
    short = db.Column(
        db.String(SHORT_LENGTH), unique=True, nullable=False
    )
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def get(short_link):
        return URLMap.query.filter_by(short=short_link).first()

    @staticmethod
    def short_validator(short):
        if len(short) > SHORT_LENGTH:
            raise ShortIsBadException(WRONG_LENGTH_IN_SHORT)
        if not fullmatch(SHORT_REXEXP, short):
            raise ShortIsBadException(SHORT_DOESNT_SUITE_REGEXP)
        if URLMap.get(short):
            raise ShortIsExistsException(SHORT_IS_EXISTS)
        return short

    @staticmethod
    def short_link_generator(counter=RANDOM_GEN_TRYS):
        for _ in range(counter):
            new_short = ''.join(
                choices(APPROVED_SYMBOLS, k=SHORT_RANDOM_LENGTH)
            )
            if not URLMap.get(new_short):
                return new_short
        raise GeneratedShortException(GENERATING_IS_FALLED)

    @staticmethod
    def db_writer(original_link, short, do_validate=False):
        if do_validate and (len(original_link) > ORIGINAL_LINK_LENGTH):
            raise LongURLIsBadException(ORIGINAL_LINK_IS_BIG)
        if short is None or short == '':
            short = URLMap.short_link_generator()
        elif do_validate:
            URLMap.short_validator(short)
        url_map = URLMap(
            original=original_link,
            short=short
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map
