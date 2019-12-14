import phonenumbers as phonenumbers
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    login = StringField('Логин',
                        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Эл. адрес',
                        validators=[DataRequired(), Email()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    phone = StringField('Номер телефона', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_phone(self, field):
        if len(field.data) > 16:
            raise ValidationError('Некорректный номер телефона!')
        try:
            input_number = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Некорректный номер телефона!')
        except:
            raise ValidationError('Некорректный номер телефона!')

    def validate_login(self, login):
        user = User.query.filter_by(login=login.data).first()
        if user:
            raise ValidationError('Пользователь с таким логином уже существует!', 'danger')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Пользователь с таким эл. адресом уже существует!')


class LoginForm(FlaskForm):
    login = StringField('Логин',
                        validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class ConfigsForm(FlaskForm):
    color = SelectField('Цвет', choices=[('beige', 'Бежевый'), ('white', 'Белый'), ('bordo', 'Бордовый'),
                                         ('light_blue', 'Голубой'), ('yellow', 'Желтый'), ('green', 'Зеленый'),
                                         ('gold', 'Золотой'), ('brown', 'Коричневый'), ('red', 'Красный'),
                                         ('orange', 'Оранжевый'), ('pink', 'Розовый'), ('silver', 'Серебристый'),
                                         ('gray', 'Серый'), ('blue', 'Синий'), ('violet', 'Фиолетовый'),
                                         ('black', 'Черный')])
    prod = SelectField('Бренд', choices=[('all', 'Любой'), ('ADMIRAL', 'ADMIRAL'), ('APP', 'APP'), ('Colomix', 'Colomix'),
                                         ('Dalux', 'Dalux'), ('Duxone', 'Duxone'), ('Dyna', 'Dyna'), ('DYO', 'DYO'),
                                         ('Luxura', 'Luxura'), ('Maxytone', 'Maxytone'), ('Mipa', 'Mipa'),
                                         ('Mixon', 'Mixon'), ('Mobihel', 'Mobihel'), ('Novol', 'Novol'),
                                         ('Profix', 'Profix'), ('PYRAMID', 'PYRAMID'), ('Quickline', 'Quickline'),
                                         ('Sadolin', 'Sadolin'), ('Sellack', 'Sellack'), ('Solid', 'Solid'),
                                         ('Unicolor', 'Unicolor'), ('Vika', 'Vika'), ('YATU', 'YATU'),
                                         ('Kartex', 'Kartex'), ('Mipa', 'Mipa'), ('Profix', 'Profix')])
    base = SelectField('Категория', choices=[('all', 'Любая'), ('acryl', 'Акриловая эмаль'), ('alkid', 'Алкидная эмаль'),
                                             ('poli', 'Полиуретановая эмаль'), ('basecov', 'Базовые покрытия')])
    min_price = IntegerField('Минимальная цена', default=0)
    max_price = IntegerField('Максимальная цена', default=8000)
    submit = SubmitField('Поиск')


class UpdateAccountForm(FlaskForm):
    login = StringField('Логин',
                        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Эл. адрес',
                        validators=[DataRequired(), Email()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    phone = StringField('Номер телефона', validators=[DataRequired()])
    submit = SubmitField('Сохранить')

    def validate_phone(self, field):
        if len(field.data) > 16:
            raise ValidationError('Некорректный номер телефона!')
        try:
            input_number = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Некорректный номер телефона!')
        except:
            raise ValidationError('Некорректный номер телефона!')

    def validate_login(self, login):
        if login.data != current_user.login:
            user = User.query.filter_by(login=login.data).first()
            if user:
                raise ValidationError('Пользователь с таким логином уже существует!', 'danger')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Пользователь с таким эл. адресом уже существует!')


