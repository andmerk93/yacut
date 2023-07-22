from flask import abort, flash, redirect, request, render_template, url_for

from yacut import app
from .forms import FLASH_MESSAGE_FOR_SHORT_LINK, URLForm
from .models import URLMap


@app.route('/', methods=['POST', 'GET'])
def add_link_view():
    form = URLForm()
    if request.method == 'GET' or not form.validate_on_submit():
        return render_template('index.html', form=form)
    original_link = form.original_link.data
    short_link = form.custom_id.data
    try:
        link_record = URLMap().db_writer(original_link, short_link)
    except Exception:
        flash(FLASH_MESSAGE_FOR_SHORT_LINK.format(short_link))
        return render_template('index.html', form=form)
    new_short = url_for(
        'link_redirect_view', short_url=link_record.short, _external=True
    )
    return render_template(
        'link_generated.html',
        form=form,
        new_short=new_short
    )


@app.route('/<string:short_url>')
def link_redirect_view(short_url):
    link_record = URLMap.get_by_short_link(short_url)
    if link_record is None:
        abort(404)
    return redirect(link_record.original)
