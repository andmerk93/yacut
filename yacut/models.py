from datetime import datetime
from random import choices
from re import fullmatch

from . import db
from .consts import (
    APPROVED_SYMBOLS,
    ORIGINAL_LINK_LENGTH,
    RANDOM_GEN_TRYS,
    SHORT_LINK_LENGTH,
    SHORT_LINK_RANDOM_LENGTH,
    SHORT_LINK_REXEXP,
)
from .error_handlers import LongURLExistsException, ShortURLIsBadException


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(
        db.String(ORIGINAL_LINK_LENGTH), unique=True, nullable=False
    )
    short = db.Column(
        db.String(SHORT_LINK_LENGTH), unique=True, nullable=False
    )
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def get(short_link):
        return URLMap.query.filter_by(short=short_link).first()

    def validator(original_link, short):
        if len(original_link) > ORIGINAL_LINK_LENGTH:
            raise LongURLExistsException
        if len(short) > SHORT_LINK_LENGTH:
            raise ShortURLIsBadException
        if not fullmatch(SHORT_LINK_REXEXP, short):
            raise ShortURLIsBadException
        if URLMap.get(short):
            raise ShortURLIsBadException
        return short

    def short_link_generator(counter=RANDOM_GEN_TRYS):
        for _ in range(counter):
            new_short = ''.join(
                choices(APPROVED_SYMBOLS, k=SHORT_LINK_RANDOM_LENGTH)
            )
            if URLMap.get(new_short):
                pass
            else:
                return new_short
        raise ShortURLIsBadException

    def db_writer(self, original_link, short_link, do_validate=False):
        if URLMap.query.filter_by(original=original_link).first():
            raise LongURLExistsException
        if short_link is None or short_link == '':
            short_link = URLMap.short_link_generator()
        elif do_validate:
            URLMap.validator(original_link, short_link)
        self.original = original_link
        self.short = short_link
        db.session.add(self)
        db.session.commit()
        return self
