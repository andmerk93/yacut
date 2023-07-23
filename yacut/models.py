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

    def short_link_is_ok(short_link):
        if (
            len(short_link) <= SHORT_LINK_LENGTH and
            fullmatch(SHORT_LINK_REXEXP, short_link) and
            not URLMap.get(short_link)
        ):
            return True

    def short_link_generator(counter=RANDOM_GEN_TRYS):
        while counter > 0:
            new_short = ''.join(
                choices(APPROVED_SYMBOLS, k=SHORT_LINK_RANDOM_LENGTH)
            )
            counter -= 1
            if URLMap.short_link_is_ok(new_short):
                break
        return new_short

    def db_writer(self, original_link, short_link):
        if URLMap.query.filter_by(original=original_link).first():
            raise LongURLExistsException
        if short_link is None or short_link == '':
            short_link = URLMap.short_link_generator()
        if not URLMap.short_link_is_ok(short_link):
            raise ShortURLIsBadException
        self.original = original_link
        self.short = short_link
        db.session.add(self)
        db.session.commit()
        return self
