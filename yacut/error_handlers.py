from flask import render_template

from yacut import app, db


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error_message='404'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error.html', error_message='500'), 500
