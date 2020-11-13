from src.hero import Hero
from src.user import User
# from src.monster import Monster

import globals
from flask import render_template, request, redirect, url_for
# from markupsafe import escape


# ##########################
# ## ERROR CODE HANDLING
# ##########################

@globals.app.errorhandler(400)
def error_page_400(_event):
    """ Handle code status 400 with 400.html page """
    return render_template('400.html'), 400


@globals.app.errorhandler(404)
def error_page_404(_event):
    """ Handle code status 404 with 404.html page """
    return render_template('404.html'), 404


@globals.app.errorhandler(500)
def error_page_500(_event):
    """ Handle code status 500 with 500.html page """
    return render_template('500.html'), 500

# ##########################
# ## VIEW HANDLING
# ##########################


@globals.app.route('/', methods=['POST', 'GET'])
def home_page():
    """ Handle GET / and POST / request, Home page function """
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
    """ Handle GET /register and POST /register request, Register page function """
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
    """ Handle GET /login and POST /login request, Login page function """
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


@globals.app.route('/user', methods=['POST', 'GET'])
def user_page():
    """ Handle POST /user and GET /user request, User profile page function """
    if globals.user is None:
        return redirect(url_for('home_page'))

    if request.method == 'POST':
        if "hero_selected" in request.form:
            for hero in globals.user.heroes:
                if hero.name == request.form['hero_selected']:
                    globals.user.selected_hero = hero

        if "hero_name" in request.form:
            globals.user.selected_hero(globals.user.get_hero_by_name(request.form['hero_name']))

    return render_template(
        'user.html',
        user=globals.user,
        heroes=globals.user.heroes
    )


@globals.app.route('/game', methods=['POST', 'GET'])
def game_page():
    """ Handle POST /game and GET /game request, Game display page function """
    if globals.user is None:
        return redirect(url_for('home_page'))

    if globals.user.selected_hero is None:
        return redirect(url_for('home_page'))

    step_context = globals.generate_step_context()

    return render_template(
        'game.html',
        user=globals.user,
        step_display=step_context['step_display'],
        step_context_title=step_context['step_context_title'],
        step_context_text=step_context['step_context_text'],
        step_options=step_context['step_context_options'],
        log=globals.log[-1] if globals.log else None
    )


@globals.app.route('/game_over')
def game_over_page():
    """ Handle GET /game_over, game over page function """
    if globals.user is None:
        return redirect(url_for('home_page'))

    return render_template("game_over.html")


@globals.app.route('/end_game')
def end_game_page():
    """ Handle GET /end_game, end of the game page function """
    if globals.user is None:
        return redirect(url_for('home_page'))

    return render_template("end_game.html")

# ##########################
# ## METHOD HANDLING
# ##########################


@globals.app.route('/logout')
def logout_page():
    """ Handle GET /logout request, Logout function """
    if globals.user is None:
        return redirect(url_for('home_page'))
    else:
        globals.user = None

    return redirect(url_for('home_page'))


@globals.app.route('/deleteAccount', methods=['POST'])
def delete_account():
    """ Handle POST /deleteAccount request, User account deletion function """
    if globals.user is None:
        return redirect(url_for('home_page'))

    if request.method == 'POST':
        if "password" in request.form:
            User.delete(globals.user.name, request.form['password'], globals.user)
            globals.user = None

            return redirect(url_for("home_page"))

    return redirect(url_for("user_page"))


@globals.app.route('/delete_hero', methods=['POST'])
def delete_hero():
    """ Handle POST /delete_hero, hero deletion function """
    if globals.user is None:
        return redirect(url_for('home_page'))

    if request.method == 'POST':
        if "hero_selected" in request.form:
            result = globals.user.get_hero_by_name(request.form['hero_selected'])
            if result:
                if globals.user.selected_hero == result:
                    globals.user.selected_hero = None

                for hero in globals.user.heroes:
                    if hero.name == request.form['hero_selected']:
                        hero.delete()
                        globals.user.heroes.remove(hero)

    return redirect(url_for('user_page'))


@globals.app.route('/create_hero', methods=['POST'])
def create_hero():
    """ Handle POST /create_hero request, hero creation function """
    if globals.user is None:
        return redirect(url_for('home_page'))

    if request.method == 'POST':
        if Hero.check_hero_available(request.form['name_of_the_hero']):
            globals.pp.pprint(f"sex input : {request.form}")
            tmp_hero = Hero(
                request.form['name_of_the_hero'],  # name
                1,  # lvl
                request.form['weapon_of_the_hero'],  # weapon
                10,  # armor
                request.form['passive_of_the_hero'],  # passive
                globals.user.id,  # user_id
                True if request.form['sex_of_the_hero'] == 'female' else False,  # sex
                1,  # current_quest
                1  # current_step
            )
            tmp_hero.load_to_db()
            globals.user.add_hero(tmp_hero)

    return redirect(url_for("user_page"))


@globals.app.route('/game_compute', methods=['POST'])
def game_compute():
    """ Handle POST /game_compute, Game computing function """
    if globals.user is None:
        return redirect(url_for('home_page'))

    if globals.user.selected_hero is None:
        return redirect(url_for('home_page'))

    if request.method == 'POST':
        if "reset_quest" in request.form:
            globals.user.selected_hero.current_quest = 1
            globals.user.selected_hero.current_step = 1

        if "userChoice" in request.form:
            log = eval(f"globals.quest{globals.user.selected_hero.current_quest}")(request.form['userChoice'])
            globals.log.append(log)
            if not log:
                return redirect(url_for("game_over_page"))

            elif log == "end_game":
                return redirect(url_for("end_game_page"))

    return redirect(url_for("game_page"))
