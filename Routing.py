import pprint

from src.database import Database
from src.hero import Hero
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


@globals.app.route('/deleteAccount', methods=['POST'])
def delete_account():
    if globals.user is None:
        return redirect(url_for('home_page'))

    if request.method == 'POST':
        if "password" in request.form :
            User.delete(globals.user.name, request.form['password'],globals.user)
            globals.user = None
            return redirect(url_for("home_page"))
    return redirect(url_for("user_page"))

@globals.app.route('/create_hero', methods=['POST'])
def create_hero():
    if globals.user is None:
        return redirect(url_for('home_page'))

    if request.method == 'POST':
        hero_name = request.form['name_of_the_hero']
        hero_weapon = request.form['weapon_of_the_hero']
        hero_passive = request.form['passive_of_the_hero']
        hero_sex = request.form['sex_of_the_hero']
        hero_user_id = globals.user.id
        hero = Hero(hero_name,1,hero_weapon,10,hero_passive,hero_user_id,hero_sex,1,0)
        hero.load_to_db() #Save the hero in the database
        globals.user.add_hero(hero)
        return redirect(url_for("user_page"))

    return redirect(url_for("user_page"))

@globals.app.route('/user', methods=['POST', 'GET'])
def user_page():
    if globals.user is None:
        return redirect(url_for('home_page'))

    if request.method == 'POST':
        if "hero_selected" in request.form:
            for hero in globals.user.heroes:
                if hero.name == request.form['hero_selected']:
                    globals.user.selected_hero = hero

    return render_template(
        'user.html',
        user=globals.user,
        heroes=globals.user.heroes
    )

# ######################

# text = db.request() : => string
# var[] = text.foundVariable() # if {% heros.sex %}
# sex = var[0][0].Attr(var[0][1])
#
# {
#     "sex" : True
#     "live" : 1000
# }
#
# maList
# maList.__getattribute__("count")()

# ######################

# init game
# display current game step
# hanlde user choice
# next step
# how to handle fight LOOP ( special template for fight loop )


@globals.app.route('/game', methods=['POST', 'GET'])
def game_page():
    print("In game_page()")
    """ This route handle game interface """
    if globals.user is None:
        return redirect(url_for('home_page'))

    #if globals.user.selected_hero is None:
        #return redirect(url_for('home_page'))

    log = None
    user_choice = None
    tmp = ["", "", ""]  # TODO use dict


    # current_quest :
    #hero = globals.user.selected_hero

    print("In game_page() 2")
    #locals()[f"quest{hero.current_quest}"](step_display, step_context_title, step_context_text)
    eval(f"globals.quest{1}")(tmp)
    print(f"display : #{tmp[0]}#")

    return render_template(
        'game.html',
        user=globals.user,
        step_display=None,
        step_context_title=None,
        step_context_text=None,
        log=log,
        questbook=None
    )


@globals.app.route('/game_compute', methods=['POST'])
def game_compute():
    """ This route handle game interaction """
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

    #quest2step2_diplay
    # step_display
    # step_context_title
    # step_context_text

    # return redirect(
    #     'game.html',s
    #     user=globals.user,
    #     lastChoice=user_choice,
    #     log=log,
    #     questbook=globals.questbook
    # )
    pass
