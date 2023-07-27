from flask import jsonify, render_template, make_response

from . import app, db


class URLMapException(Exception):
    pass


class LongURLIsBadException(URLMapException):
    pass


class ShortIsBadException(URLMapException):
    pass


class ShortIsExistsException(URLMapException):
    pass


class GeneratedShortException(ShortIsBadException):
    pass


@app.errorhandler(URLMapException)
def bad_news_teller(error, status=400):
    message = error.args[0]
    if len(error.args) == 2:
        status = error.args[1]
    return make_response(jsonify(dict(message=message)), status)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error_message='404'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error.html', error_message='500'), 500
