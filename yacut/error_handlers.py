from flask import jsonify, render_template

from . import app, db

NOT_FOUND_TEXT = 'Нет такой страницы'
SERVER_ERROR_TEXT = 'Ошибка сервера'


class URLMapException(Exception):
    pass


class ShortIsBadException(URLMapException):
    pass


class ShortIsExistsException(URLMapException):
    pass


class GeneratedShortException(URLMapException):
    pass


class APIException(Exception):

    def __init__(self, message, status_code=None):
        self.message = message
        self.status_code = status_code if status_code else 400


@app.errorhandler(APIException)
def bad_news_teller(error):
    return jsonify(dict(message=error.message)), error.status_code


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error_message=NOT_FOUND_TEXT), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error.html', error_message=SERVER_ERROR_TEXT), 500
