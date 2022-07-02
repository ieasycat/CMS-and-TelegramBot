from app import app
from app.models.forms import RegistrationForm, LoginForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models.dbmodels import Manager
from app.controllers.user_db_controller import ManagerController
from app.controllers.email_controller import EmailController
from flask import redirect, url_for, flash, render_template
from flask_login import current_user, login_user, logout_user


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()

    if current_user.is_authenticated:
        return redirect((url_for('main_page')))

    if form.validate_on_submit():
        ManagerController.add_manager(form=form)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('authorization/registration.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect((url_for('main_page')))

    form = LoginForm()

    if form.validate_on_submit():
        user = ManagerController.get_manager(email=form.email.data)
        check_manager = ManagerController.check_manager(user=user, password=form.password.data)

        if check_manager:
            flash('Invalid username or password')
            return check_manager

        login_user(user, remember=form.remember_me.data)

        return redirect(url_for('main_page'))

    return render_template('authorization/login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))

    form = ResetPasswordRequestForm()

    if form.validate_on_submit():
        user = ManagerController.get_manager(email=form.email.data)

        if user:
            EmailController.send_password_reset_email(user=user)

        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))

    return render_template('authorization/reset_password_request.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token: str):
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))

    user = Manager.verify_reset_password_token(token=token)

    if not user:
        return redirect(url_for('main_page'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        ManagerController.change_password(user=user, new_password=form.password.data)
        flash('Your password has been reset.')
        return redirect(url_for('login'))

    return render_template('authorization/reset_password.html', form=form)
