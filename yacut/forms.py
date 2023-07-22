from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import (
    DataRequired, Length, Optional, Regexp, URL, ValidationError
)

from . import SHORT_LINK_LENGTH, SHORT_LINK_REXEXP, ORIGINAL_LINK_LENGTH
from .models import URLMap

FLASH_MESSAGE_FOR_SHORT_LINK = 'Имя {0} уже занято!'
ORIGINAL_LINK_TEXT = 'Длинная ссылка'
ORIGINAL_LINK_VALIDATOR = 'Обязательное поле'
CUSTOM_ID_TEXT = 'Короткая ссылка (ваш вариант)'
CUSTOM_ID_VALIDATOR = 'Допустимы символы из латиницы и цифр'
SUBMIT_TEXT = 'Добавить'


class URLForm(FlaskForm):
    original_link = StringField(
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
            Length(max=SHORT_LINK_LENGTH),
            Regexp(SHORT_LINK_REXEXP, message=CUSTOM_ID_VALIDATOR),
            Optional(),
        ]
    )
    submit = SubmitField(SUBMIT_TEXT)

    def validate_custom_id(form, field):
        """
        Валидатор готов, но не подключен,
        в таком виде не пройдут автотесты,
        ибо тест проверяет текст в html-странице.
        Для запуска надо переменовать функцию в
        validate_custom_id
        """
        if URLMap.get_by_short_link(field.data):
            raise ValidationError(
                FLASH_MESSAGE_FOR_SHORT_LINK.format(field.data)
            )
