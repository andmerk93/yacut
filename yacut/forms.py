from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, URL


class URLForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'), URL()]
    )
    custom_id = StringField(
        'Короткая ссылка (ваш вариант)',
        validators=[Length(2, 16), Optional()]
    )
    submit = SubmitField('Добавить')
