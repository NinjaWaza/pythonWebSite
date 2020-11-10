import pprint
from src.user import User
from src.monster import Monster

import globals
from flask import Flask, render_template, request, redirect, url_for
from markupsafe import escape


@globals.app.errorhandler(400)
def error_page_400(_event):
    return render_template('400.html'), 400


@globals.app.errorhandler(404)
def error_page_404(_event):
    return render_template('404.html'), 404


@globals.app.errorhandler(500)
def error_page_500(_event):
    return render_template('500.html'), 500


@globals.app.route('/', methods=['POST', 'GET'])
def home_page():
    if globals.user is not None:
        return redirect(url_for('user_page'))

    if request.method == "POST":
        if "login" in request.form:
            return redirect(url_for('login_page'))
        elif "register" in request.form:
            return redirect(url_for('register_page'))

    return render_template(
        'index.html',
        user=globals.user
    )


@globals.app.route('/register', methods=['POST', 'GET'])
def register_page():
    if globals.user is not None:
        return redirect(url_for('user_page'))

    error_messages = list()

    if request.method == 'POST':
        if 'username_input' and 'password_input' and 'password_confirm_input' in request.form:
            if request.form['password_input'] == request.form['password_confirm_input']:
                register = User.register(request.form['username_input'], request.form['password_input'])

                if isinstance(register, User):
                    globals.user = register
                    return redirect(url_for('user_page'))
                else:
                    error_messages.append(register)
            else:
                error_messages.append("password confirmation must match password")

    return render_template(
        'register.html',
        user=globals.user,
        error_messages=error_messages
    )


@globals.app.route('/login', methods=['POST', 'GET'])
def login_page():
    if globals.user is not None:
        return redirect(url_for('user_page'))

    error_messages = list()

    if request.method == 'POST':
        if 'username_input' and 'password_input' in request.form:
            login = User.login(request.form['username_input'], request.form['password_input'])
            if not isinstance(login, User):
                error_messages.append(login)
            else:
                globals.user = login
                return redirect(url_for('user_page'))

    return render_template(
        'login.html',
        user=globals.user,
        error_messages=error_messages
    )


@globals.app.route('/logout')
def logout_page():
    if globals.user is None:
        return redirect(url_for('home_page'))
    else:
        globals.user = None

    return redirect(url_for('home_page'))


@globals.app.route('/user', methods=['POST', 'GET'])
def user_page():
    if globals.user is None:
        return redirect(url_for('home_page'))

    if request.method == 'POST':
        pass  #  TODO : computation

    return render_template(
        'user.html',
        user=globals.user,
        the_heroes=globals.user.get_heroes()
    )

@globals.app.route('/game', methods=['POST', 'GET'])
def game_page():
    if globals.user is None:
        return redirect(url_for('home_page'))

    log = None
    user_choice = None

    if request.method == 'POST':
        if "reset_quest" in request.form:
            globals.user.set_quest(0, 0)
        elif "userChoice" in request.form:
            user_choice = request.form['userChoice']
            # execute la fonction lié au step de la quete
            log = eval('globals.quest' + str(globals.user.quest["id"]) + 'step' + str(globals.user.quest["step"]))(user_choice)

    return render_template(
        'game.html',
        user=globals.user,
        lastChoice=user_choice,
        log=log,
        questbook=globals.questbook
    )

