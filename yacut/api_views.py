from flask import jsonify, request, url_for

from . import app
from .consts import SHORT_FUNCTION_NAME
from .error_handlers import (
    ShortIsBadException, ShortIsExistsException, URLMapException
)
from .models import URLMap


EMPTY_REQUEST_JSON = 'Отсутствует тело запроса'
SHORT_ALREADY_EXISTS = 'Имя "{0}" уже занято.'
NO_URL_IN_REQUEST_JSON = '"url" является обязательным полем!'
WRONG_NAME_FOR_SHORT_URL = 'Указано недопустимое имя для короткой ссылки'
WRONG_SHORT_ID = 'Указанный id не найден'


@app.route('/api/id/<string:short_url>/', methods=['GET'])
def get_original_link_api(short_url):
    original_link = URLMap.get(short_url)
    if original_link is None:
        raise URLMapException(WRONG_SHORT_ID, 404)
    return jsonify(url=original_link.original), 200


@app.route('/api/id/', methods=['POST'])
def add_link_api():
    data = request.get_json(silent=True)
    try:
        long_url = data['url']
    except TypeError:
        raise URLMapException(EMPTY_REQUEST_JSON)
    except KeyError:
        raise URLMapException(NO_URL_IN_REQUEST_JSON)
    short = data.get('custom_id')
    try:
        link_record = URLMap().db_writer(long_url, short, do_validate=True)
    except ShortIsExistsException:
        raise URLMapException(SHORT_ALREADY_EXISTS.format(short))
    except ShortIsBadException:
        raise URLMapException(WRONG_NAME_FOR_SHORT_URL)
    return jsonify(dict(
        url=long_url,
        short_link=url_for(
            SHORT_FUNCTION_NAME,
            short_url=link_record.short,
            _external=True
        ),
    )), 201
