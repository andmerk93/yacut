from flask import abort, jsonify, request, url_for, make_response

from yacut import app
from .models import URLMap

WRONG_SHORT_ID = 'Указанный id не найден'
EMPTY_REQUEST_JSON = 'Отсутствует тело запроса'
NO_URL_IN_REQUEST_JSON = '"url" является обязательным полем!'
LONG_URL_ALREADY_EXISTS = 'Имя "{0}" уже занято.'
WRONG_NAME_FOR_SHORT_URL = 'Указано недопустимое имя для короткой ссылки'


def bad_news_teller(testing_object=None, message='Unknown error', status=400):
    if testing_object is None:
        abort(make_response(jsonify(dict(message=message)), status))


@app.route('/api/id/<string:short_url>/', methods=['GET'])
def get_original_link_api(short_url):
    original_link = URLMap.get_by_short_link(short_url)
    bad_news_teller(original_link, WRONG_SHORT_ID, 404)
    return jsonify(url=original_link.original), 200


@app.route('/api/id/', methods=['POST'])
def add_link_api():
    data = request.get_json(silent=True)
    bad_news_teller(data, EMPTY_REQUEST_JSON)
    long_url = data.get('url')
    bad_news_teller(long_url, NO_URL_IN_REQUEST_JSON)
    short_url = data.get('custom_id')
    try:
        link_record = URLMap().db_writer(long_url, short_url)
    except Exception as exc:
        commit_status = exc.args[0]
        if commit_status == 'long_url_exists':
            bad_news_teller(message=LONG_URL_ALREADY_EXISTS.format(short_url))
        if commit_status == 'short_url_is_bad':
            bad_news_teller(message=WRONG_NAME_FOR_SHORT_URL)
    return jsonify(dict(
        url=link_record.original,
        short_link=url_for(
            'link_redirect_view',
            short_url=link_record.short,
            _external=True
        ),
    )), 201
