from flask import abort, flash, redirect, render_template, url_for

from . import app
from .consts import SHORT_LINK_FUNCTION_NAME
from .error_handlers import URLMapException
from .forms import FLASH_MESSAGE_FOR_SHORT_LINK, URLForm
from .models import URLMap


@app.route('/', methods=['POST', 'GET'])
def add_link_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    original_link = form.original_link.data
    short_link = form.custom_id.data
    try:
        link_record = URLMap().db_writer(original_link, short_link, called_from_form=True)
    except URLMapException:
        flash(FLASH_MESSAGE_FOR_SHORT_LINK.format(short_link))
        return render_template('index.html', form=form)
    full_short_link = url_for(
        SHORT_LINK_FUNCTION_NAME, short_url=link_record.short, _external=True
    )
    return render_template(
        'index.html',
        form=form,
        full_short_link=full_short_link
    )


@app.route('/<string:short_url>')
def link_redirect_view(short_url):
    link_record = URLMap.get(short_url)
    if link_record is None:
        abort(404)
    return redirect(link_record.original)
