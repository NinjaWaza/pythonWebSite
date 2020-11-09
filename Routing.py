import pprint

from globals import *
from flask import Flask, render_template, request
from markupsafe import escape


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/game', methods=['POST', 'GET'])
def game_page():
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
        lastChoice=user_choice,
        log=log,
        user=globals.user,
        questbook=globals.questbook
    )

