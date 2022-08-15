from flask import Flask, render_template, make_response, jsonify, request
from flask_login import LoginManager, login_required
import flask_login, flask
import json, requests, os
import time
from time import time

app = Flask(__name__)
app.secret_key = 'waterdishow'
#login
login_manager = LoginManager()
login_manager.init_app(app)

users = {'test': {'password': 'password'}}

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = flask.request.form['username']
    if username in users and flask.request.form['password'] == users[username]['password']:
        user = User()
        user.id = username
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('index'))

    return 'Bad login'

@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@app.route('/add')
@flask_login.login_required
def add():
    return render_template('add.html')

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('index'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401
#endlogin

@app.route('/postdata', methods=["GET", "POST"])
def postdata():
    if request.method == 'POST':
        data = request.json
    return data

@app.route('/dataapi', methods=["GET", "POST"])
def dataapi():
    url = requests.get("http://www.randomnumberapi.com/api/v1.0/random?min=0&max=25&count=10")
    text = url.text
    data = json.loads(text)
    user=[
        # {"Station":"OP1","Phase":"Phase 1", "Data":[{"id":"HC-K1", "Water":data[0], "Temp":data[3], "Status":True},
        #                                               {"id":"HC-K2", "Water":data[1], "Temp":data[2], "Status":True},
        #                                               {"id":"Mole Cleaning 1", "Water":data[5], "Temp":data[9], "Status":False},
        #                                               {"id":"Mole Cleaning 2", "Water":data[4], "Temp":data[8], "Status":True},
        #                                               {"id":"Mole Cleaning 3", "Water":data[6], "Temp":data[7], "Status":True}]},
        #   {"Station":"OP1","Phase":"Phase 2", "Data":[{"id":"K1", "Water":data[1], "Temp":data[2], "Status":False},
        #                                               {"id":"K2-1", "Water":data[4], "Temp":data[5], "Status":False},
        #                                               {"id":"K2-2", "Water":data[6], "Temp":data[3], "Status":True},
        #                                               {"id":"AI TECH1", "Water":data[0], "Temp":data[9], "Status":True},
        #                                               {"id":"Ulaka", "Water":data[7], "Temp":data[8], "Status":False},
        #                                               {"id":"HC-K3", "Water":data[0], "Temp":data[1], "Status":True},
        #                                               {"id":"HC-K4", "Water":data[2], "Temp":data[9], "Status":False},]},
        #   {"Station":"OP1","Phase":"Phase 7", "Data":[{"id":"Mole Cleaning", "Water":data[0], "Temp":data[9], "Status":True},
        #                                               {"id":"AI TECH", "Water":data[1], "Temp":data[8], "Status":True},
        #                                               {"id":"HC-OPTIMAL", "Water":data[2], "Temp":data[7], "Status":True},]},
          {"Station":"OP2","Phase":"Phase 4", "Data":[{"id":"ROBOT", "Water":data[5], "Temp":data[6], "Status":True},
                                                      {"id":"Fisa 2", "Water":data[4], "Temp":data[7], "Status":False},
                                                      {"id":"Fisa 4", "Water":data[3], "Temp":data[8], "Status":True},]},
          {"Station":"OP2","Phase":"Phase 5", "Data":[{"id":"L15 Station 1", "Water":data[9], "Temp":data[8], "Status":True},
                                                      {"id":"L15 Station 2", "Water":data[6], "Temp":data[7], "Status":False},
                                                      {"id":"Fisa 3", "Water":data[5], "Temp":data[4], "Status":False},
                                                      {"id":"L13", "Water":data[2], "Temp":data[3], "Status":True},
                                                      {"id":"L14", "Water":data[1], "Temp":data[0], "Status":True},]},
          {"Station":"OP2","Phase":"Phase 9", "Data":[{"id":"HC-4", "Water":data[0], "Temp":data[1], "Status":True},
                                                      {"id":"HC-5 Station 1", "Water":data[2], "Temp":data[3], "Status":False},
                                                      {"id":"HC-5 Station 2", "Water":data[5], "Temp":data[4], "Status":False},
                                                      {"id":"AI", "Water":data[6], "Temp":data[7], "Status":True},
                                                      {"id":"HC-3", "Water":data[8], "Temp":data[1], "Status":True},
                                                      {"id":"HC-6", "Water":data[0], "Temp":data[9], "Status":False},]},
          ]
    response = make_response(json.dumps(user))
    response.content_type = 'application/json'
    return jsonify(user)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/line')
def line():
    return render_template('line.html')

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/alert')
def alert():
    return render_template('alert.html')

if __name__ == "__main__":
    app.run(debug=True)