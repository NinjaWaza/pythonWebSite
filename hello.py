from flask import Flask, request, render_template
app = Flask(__name__)

#When we call the main route, that will call the main template aka (mainPage.html)
@app.route('/')
def hello_world():
    return render_template('mainPage.html')

@app.route('/test')
def my_form():
    return render_template('my-form.html')

#When we call /test route with the post method
@app.route('/test', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    return processed_text
