from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Введите длинную ссылку',
        validators=[DataRequired(message='Обязательное поле'),
                    URL(message='Некорректный URL')]
    )
    custom_id = StringField(
        'Введите вариант короткой ссылки',
        validators=[Length(max=6), Optional(),
                    Regexp(regex=r'^[a-zA-Z\d]{1,16}$',
                    message='Только латинские буквы и цифры от 0 до 9')]
    )
    submit = SubmitField('Сгенерировать')
