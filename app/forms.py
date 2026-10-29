from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, Optional

SUBJECT_CHOICES = [
    ("", "— Оберіть тему —"),
    ("question", "Загальне питання"),
    ("cooperation", "Співпраця"),
    ("bug", "Повідомлення про помилку"),
    ("other", "Інше"),
]


class ContactForm(FlaskForm):
    name = StringField(
        "Ваше ім'я",
        validators=[
            DataRequired(message="Вкажіть ім'я."),
            Length(min=2, max=50, message="Ім'я має містити від 2 до 50 символів."),
        ],
    )
    email = StringField(
        "Email адреса",
        validators=[
            DataRequired(message="Вкажіть email."),
            Regexp(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", message="Невірний формат email."),
            Length(max=120, message="Email занадто довгий."),
        ],
    )
    phone = StringField(
        "Телефон (необов'язково)",
        validators=[
            Optional(),
            Regexp(r"^\+?[0-9\s\-()]{7,20}$", message="Невірний формат телефону."),
        ],
    )
    subject = SelectField(
        "Тема",
        choices=SUBJECT_CHOICES,
        validators=[DataRequired(message="Оберіть тему повідомлення.")],
    )
    message = TextAreaField(
        "Повідомлення",
        validators=[
            DataRequired(message="Напишіть повідомлення."),
            Length(min=10, max=1000, message="Повідомлення має містити від 10 до 1000 символів."),
        ],
    )
    submit = SubmitField("Відправити")