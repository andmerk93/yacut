from flask import jsonify, request, url_for

from yacut import app
from .models import URLMap, db_writer, short_link_generator


def bad_news_teller(message, status=400):
    return jsonify(dict(message=message)), status


@app.route('/api/id/<string:short_url>/', methods=['GET'])
def get_original_link_api(short_url):
    original_link = URLMap.query.filter_by(short=short_url).first()
    if original_link is None:
        return bad_news_teller('Указанный id не найден', 404)
    return jsonify({'url': original_link.original}), 200


@app.route('/api/id/', methods=['POST'])
def add_link_api():
    data = request.get_json(silent=True)
    if data is None:
        return bad_news_teller('Отсутствует тело запроса')
    long_url = data.get('url')
    if long_url is None:
        return bad_news_teller('"url" является обязательным полем!')
    short_url = data.get('custom_id')
    if short_url is None or short_url == '':
        short_url = short_link_generator()
    commit_status, link_record = db_writer(long_url, short_url)
    if commit_status == 'long_url_exists':
        return bad_news_teller(f'Имя "{short_url}" уже занято.')
    if commit_status == 'short_url_is_bad':
        return bad_news_teller('Указано недопустимое имя для короткой ссылки')
    return jsonify(dict(
        url=link_record.original,
        short_link=url_for(
            'link_redirect_view',
            short_url=link_record.short,
            _external=True
        ),
    )), 201
