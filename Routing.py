from src.classes.hero import Hero
from src.classes.user import User
import src.computing_quest

import globals
from flask import render_template, request, redirect, url_for


# ##########################
# ## ERROR CODE HANDLING
# ##########################

@globals.app.errorhandler(400)
def error_page_400(_event):
    """ Handle code status 400 with 400.html page """
    return render_template('400.html', user=globals.user), 400


@globals.app.errorhandler(404)
def error_page_404(_event):
    """ Handle code status 404 with 404.html page """
    return render_template('404.html', user=globals.user), 404


@globals.app.errorhandler(500)
def error_page_500(_event):
    """ Handle code status 500 with 500.html page """
    return render_template('500.html', user=globals.user), 500


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

    return render_template(
        'user.html',
        user=globals.user,
        heroes=globals.user.heroes,
        questbook=globals.questbook
    )


@globals.app.route('/game', methods=['GET'])
def game_storytelling_page():
    """ Handle GET /game request, Game display page function """
    if globals.user is None:
        return redirect(url_for('home_page'))

    if globals.user.selected_hero is None:
        return redirect(url_for('home_page'))

    step_context = globals.generate_step_context()

    return render_template(
        'game_storytelling.html',
        user=globals.user,
        step_display=step_context['step_display'],
        step_context_title=step_context['step_context_title'],
        step_context_text=step_context['step_context_text'],
        step_options=step_context['step_context_options'],
        logs=globals.logs
    )


@globals.app.route('/fight', methods=['GET'])
def game_fight_page():
    """ Handle GET /fight request, Game fight display page function """
    if globals.user is None:
        return redirect(url_for('home_page'))

    if globals.user.selected_hero is None:
        return redirect(url_for('home_page'))

    fight_context = globals.generate_fight_context()

    return render_template(
        'game_fight.html',
        user=globals.user,
        fight_display=fight_context['fight_display'],
        fight_context_title=fight_context['fight_context_title'],
        fight_context_text=fight_context['fight_context_text'],
        fight_context_options=fight_context['fight_context_options'],
        fight_state=globals.fight_state,
        logs=globals.logs
    )


@globals.app.route('/game_over')
def game_over_page():
    """ Handle GET /game_over, game over page function """
    if globals.user is None:
        return redirect(url_for('home_page'))

    return render_template("game_over.html", user=globals.user)


@globals.app.route('/end_game')
def end_game_page():
    """ Handle GET /end_game, end of the game page function """
    if globals.user is None:
        return redirect(url_for('home_page'))

    return render_template("end_game.html", user=globals.user)


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
        if Hero.check_hero_available(request.form['new_hero_name']):
            tmp_hero = Hero(
                _name=request.form['new_hero_name'],  # name
                _lvl=1,  # lvl
                _weapon=request.form['new_hero_weapon'],  # weapon
                _armor=50,  # armor TODO : Pour équilibrage
                _passive=request.form['new_hero_passive'],  # passive
                _user_id=globals.user.id,  # user_id
                _sex=request.form['new_hero_sex'],  # sex
                _quest_num=1,  # current_quest
                _step_num=1  # current_step
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
            status = eval(f"src.computing_quest.quest{globals.user.selected_hero.current_quest}")(request.form['userChoice'])

            if status == "game_over":
                return redirect(url_for("game_over_page"))

            elif status == "fight" or status == "start_fight":
                return redirect(url_for("game_fight_page"))

            elif status == "end_game":
                return redirect(url_for("end_game_page"))

        if "continue_quest" in request.form:
            if globals.questbook\
                    .get_quest_by_number(globals.user.selected_hero.current_quest)\
                    .get_step_by_number(globals.user.selected_hero.current_step).text == "Fight":
                globals.user.selected_hero.current_step -= 1

    return redirect(url_for("game_storytelling_page"))
