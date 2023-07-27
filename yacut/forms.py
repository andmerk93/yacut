from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (
    DataRequired, Length, Optional, Regexp, URL, ValidationError
)

from .consts import SHORT_LENGTH, SHORT_REXEXP, ORIGINAL_LINK_LENGTH
from .models import URLMap

FLASH_MESSAGE_FOR_SHORT_LINK = 'Имя {0} уже занято!'
ORIGINAL_LINK_TEXT = 'Длинная ссылка'
ORIGINAL_LINK_VALIDATOR = 'Обязательное поле'
CUSTOM_ID_TEXT = 'Короткая ссылка (ваш вариант)'
CUSTOM_ID_VALIDATOR = 'Допустимы символы из латиницы и цифр'
SUBMIT_TEXT = 'Добавить'


class URLForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LINK_TEXT,
        validators=[
            DataRequired(message=ORIGINAL_LINK_VALIDATOR),
            URL(),
            Length(max=ORIGINAL_LINK_LENGTH)
        ]
    )
    custom_id = StringField(
        CUSTOM_ID_TEXT,
        validators=[
            Length(max=SHORT_LENGTH),
            Regexp(SHORT_REXEXP, message=CUSTOM_ID_VALIDATOR),
            Optional(),
        ]
    )
    submit = SubmitField(SUBMIT_TEXT)

    def validate_custom_id(form, field):
        if URLMap.get(field.data):
            raise ValidationError(
                FLASH_MESSAGE_FOR_SHORT_LINK.format(field.data)
            )
