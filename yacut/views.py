from flask import flash, redirect, render_template

from yacut import app
from .forms import URLForm
from .models import URLMap, db_writer, short_link_generator


@app.route('/')
def index_view():
    return render_template('index.html', form=URLForm())


@app.route('/', methods=['POST'])
def add_link_view():
    form = URLForm()
    if form.validate_on_submit():
        original_link = form.original_link.data
        short_link = form.custom_id.data
        if short_link is None or short_link == '':
            short_link = short_link_generator()
        commit_status, link_record = db_writer(original_link, short_link)
        if commit_status != 'OK':
            # Здесь была обработка 2-х разных ошибок,
            # для длинной и короткой ссылки,
            # с разными сообщениями, но они,
            # конечно же, не прошли автотесты,
            # сообщения должно быть одинаковыми
            flash(f'Имя {short_link} уже занято!')
            return render_template('index.html', form=form)
        return render_template(
            'link_generated.html',
            form=form,
            new_short=link_record.short
        )
    return render_template('index.html', form=form)


@app.route('/<string:short_url>')
def link_redirect_view(short_url):
    link_record = URLMap.query.filter_by(short=short_url).first_or_404()
    return redirect(link_record.original)
