from datetime import datetime
from random import choices
from re import fullmatch

from . import (
    APPROVED_SYMBOLS,
    ORIGINAL_LINK_LENGTH,
    RANDOM_GEN_TRYS,
    SHORT_LINK_LENGTH,
    SHORT_LINK_RANDOM_LENGTH,
    SHORT_LINK_REXEXP,
    db
)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(
        db.String(ORIGINAL_LINK_LENGTH), unique=True, nullable=False
    )
    short = db.Column(
        db.String(SHORT_LINK_LENGTH), unique=True, nullable=False
    )
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())

    @classmethod
    def get_by_short_link(cls, short_link):
        return cls.query.filter_by(short=short_link).first()

    @classmethod
    def get_by_original_link(cls, original_link):
        return cls.query.filter_by(original=original_link).first()

    def short_link_is_ok(self, new_link=None):
        short_link = self.short
        if new_link:
            short_link = new_link
        if (
            len(short_link) <= SHORT_LINK_LENGTH and
            fullmatch(SHORT_LINK_REXEXP, short_link) and
            not self.get_by_short_link(short_link)
        ):
            return True

    def short_link_generator(self, counter=RANDOM_GEN_TRYS):
        new_link = ''.join(
            choices(APPROVED_SYMBOLS, k=SHORT_LINK_RANDOM_LENGTH)
        )
        if not self.short_link_is_ok(new_link):
            counter -= 1
            new_link = self.short_link_generator(counter)
        self.short = new_link

    def db_writer(self, original_link, short_link):
        self.original = original_link
        self.short = short_link
        if self.get_by_original_link(self.original):
            raise Exception('long_url_exists')
        if self.short is None or self.short == '':
            self.short_link_generator()
        if not self.short_link_is_ok():
            raise Exception('short_url_is_bad')
        db.session.add(self)
        db.session.commit()
        return self
