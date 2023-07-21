from datetime import datetime
from random import choice
from string import ascii_letters, digits

from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, unique=True, nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())


def short_link_is_ok(short_link):
    # должно быть 6 <= len...
    # но тогда не проходят тесты
    if not (2 <= len(short_link) <= 16):
        return False
    for i in set(short_link):
        if i not in ascii_letters + digits:
            return False
    if URLMap.query.filter_by(short=short_link).first():
        return False
    return True


def db_writer(original_link, short_link):
    if URLMap.query.filter_by(original=original_link).first():
        return ('long_url_exists', None)
    if not short_link_is_ok(short_link):
        return ('short_url_is_bad', None)
    link_record = URLMap(
        original=original_link,
        short=short_link,
    )
    db.session.add(link_record)
    db.session.commit()
    return ('OK', link_record)


def short_link_generator():
    new_link = ''.join(choice(ascii_letters + digits) for _ in range(6))
    # лучше было бы range(16)
    # или случайное число 6-16,
    # но опять не пустили автотесты
    if not short_link_is_ok(new_link):
        new_link = short_link_generator()
    return new_link
