import datetime

from flask import render_template, url_for, flash, redirect, request
from app import db, bcrypt
from app.forms import RegistrationForm, LoginForm, ConfigsForm, UpdateAccountForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required

from app import app
from app.search.searchUtils import search_utils

collection = ""

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Логин или пароль указан неверно', 'danger')
    return render_template('signin.html', title='Login', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(login=form.login.data, email=form.email.data, name=form.name.data,
                    surname=form.surname.data, phone=form.phone.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Аккаунт создан!', 'success')
        return redirect(url_for('signin'))
    return render_template('signup.html', title='Register', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.login = form.login.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.name = form.name.data
        current_user.surname = form.surname.data
        db.session.commit()
        flash('Изменения сохранены!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.login.data = current_user.login
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.name.data = current_user.name
        form.surname.data = current_user.surname
    return render_template('profile.html', title='Profile', form=form)


@app.route("/search_confs", methods=['GET', 'POST'])
def search_confs():
    if not current_user.is_authenticated:
        return redirect(url_for('register'))
    form = ConfigsForm()
    if form.validate_on_submit():
        global collection
        collection = current_user.login + "".join(str(datetime.datetime.now()).split())
        items = search_utils.search(search_utils, collection, form.color.data, form.prod.data, form.base.data,
                                    form.min_price.data, form.max_price.data)
        return redirect(url_for('results'))
    else:
        return render_template('confs.html', title='Confs', form=form)


@app.route("/results", methods=['GET', 'POST'])
def results():
    items = search_utils.Items
    if items.__len__() == 0:
        flash('По вашему запрсу ничего не найдено', 'warning')
    return render_template('results.html', items=items)


@app.route("/item/<string:item_id>")
def item(item_id):
    item = search_utils.get_item(search_utils, item_id)
    return render_template('item.html', item=item)
