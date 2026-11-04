from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DecimalField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, NumberRange
from wtforms.fields import SelectChoice

CATEGORIES = [
    SelectChoice("electronics", "Електроніка"),
    SelectChoice("clothes", "Одяг"),
    SelectChoice("books", "Книги"),
    SelectChoice("other", "Інше"),
]


class ProductForm(FlaskForm):
    name = StringField("Назва", validators=[
        DataRequired(message="Вкажіть назву."),
        Length(min=3, max=100, message="Назва має містити від 3 символів."),
    ])
    content = TextAreaField("Опис", render_kw={"rows": 5, "cols": 40},
                            validators=[DataRequired(message="Вкажіть опис.")])
    price = DecimalField("Ціна", places=2, validators=[
        InputRequired(message="Вкажіть ціну."),
        NumberRange(min=0.01, message="Ціна має бути більшою за 0."),
    ])
    category = SelectField("Категорія", choices=CATEGORIES)
    quantity = IntegerField("Кількість", validators=[
        InputRequired(message="Вкажіть кількість."),
        NumberRange(min=0, message="Кількість не може бути від'ємною."),
    ])
    image = FileField("Зображення", validators=[
        FileAllowed(["png", "jpg", "jpeg"], "Дозволені лише PNG, JPG, JPEG."),
    ])
    submit = SubmitField("Зберегти")