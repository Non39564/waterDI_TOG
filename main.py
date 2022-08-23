from flask import Flask, make_response, jsonify, request
from flask_login import LoginManager
import flask_login, flask
import json, requests
from flask import render_template as real_render_template
from functools import partial
from db import *

app = Flask(__name__)
app.secret_key = 'waterdishow'

error = showerror()
user_recept = show_recept()
render_template = partial(real_render_template, error=error, user_recept=user_recept)

# @app.route('/dataapi', methods=["GET", "POST"])
# def dataapi():
#     url = requests.get("http://www.randomnumberapi.com/api/v1.0/random?min=0&max=25&count=10")
#     text = url.text
#     data = json.loads(text)
#     user=[
#           {"Station":"OP2","Phase":"Phase 4", "Data":[{"id":"ROBOT", "Water":data[5], "Temp":data[6], "Status":True},
#                                                       {"id":"Fisa 2", "Water":data[4], "Temp":data[7], "Status":False},
#                                                       {"id":"Fisa 4", "Water":data[3], "Temp":data[8], "Status":True},]},
#           {"Station":"OP2","Phase":"Phase 5", "Data":[{"id":"L15 Station 1", "Water":data[9], "Temp":data[8], "Status":True},
#                                                       {"id":"L15 Station 2", "Water":data[6], "Temp":data[7], "Status":False},
#                                                       {"id":"Fisa 3", "Water":data[5], "Temp":data[4], "Status":False},
#                                                       {"id":"L13", "Water":data[2], "Temp":data[3], "Status":True},
#                                                       {"id":"L14", "Water":data[1], "Temp":data[0], "Status":True},]},
#           {"Station":"OP2","Phase":"Phase 9", "Data":[{"id":"HC-4", "Water":data[0], "Temp":data[1], "Status":True},
#                                                       {"id":"HC-5 Station 1", "Water":data[2], "Temp":data[3], "Status":False},
#                                                       {"id":"HC-5 Station 2", "Water":data[5], "Temp":data[4], "Status":False},
#                                                       {"id":"AI", "Water":data[6], "Temp":data[7], "Status":True},
#                                                       {"id":"HC-3", "Water":data[8], "Temp":data[1], "Status":True},
#                                                       {"id":"HC-6", "Water":data[0], "Temp":data[9], "Status":False},]},
#           ]
#     response = make_response(json.dumps(user))
#     response.content_type = 'application/json'
#     return jsonify(user)

########################### Function Login ###########################
login_manager = LoginManager()
login_manager.init_app(app)

users = users()

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
    if request.method == 'POST':
        if flask.request.form['check'] == "login":
            username = flask.request.form['username']
            if username in users and flask.request.form['password'] == users[username]['password']:
                user = User()
                user.id = username
                flask_login.login_user(user)
                return flask.redirect(flask.url_for('index'))
            
            errorpassword = "True"
            return render_template('index.html', sweetalert=errorpassword)
        if flask.request.form['check'] == "register":
            Name = flask.request.form['registerName']
            username = flask.request.form['registerUsername']
            password = flask.request.form['registerPassword']
            password_again = flask.request.form['registerRepeatPassword']
            if password == password_again:
                insert_Pre_User(username, Name, password)
                waitforrecept = "True"
                return render_template('index.html', waitforrecept=waitforrecept)
            else:
                notmatchpassword = "True"
                return render_template('index.html', notmatchpassword=notmatchpassword)

@app.route('/addmachine', methods=['GET', 'POST'])
@flask_login.login_required
def addmachine():
    if request.method == 'POST':
        if flask.request.form['add'] == "machine":
            id = flask.request.form['MachineId']
            ip = flask.request.form['MachineIp']
            port = flask.request.form['MachinePort']
            station = flask.request.form['inputOpMac']
            phase = flask.request.form['inputPhaseMac']
            Add_Machine(id, ip, port, station, phase)
            return flask.redirect(flask.url_for('addmachine'))
        if flask.request.form['add'] == "device":
            Machine = flask.request.form['inputMachineID']
            Site = flask.request.form['inputSite']
            Slot_Temp = flask.request.form['Slot_temp']
            Slot_Water= flask.request.form['Water']
            Add_Device(Machine, Site, Slot_Temp, Slot_Water)
            return flask.redirect(flask.url_for('addmachine'))
        if flask.request.form['add'] == "phase":
            OPadd = flask.request.form['OPadd']
            Phaseadd = flask.request.form['Phaseadd']
            Siteadd = flask.request.form['Siteadd']
            add_phase(OPadd, Phaseadd, Siteadd)
            return flask.redirect(flask.url_for('addmachine'))
        
    station = get_dropdown_values()
    machine_data = get_dropdown_values_machine()
    slot = dynamic_slot()
    edit_delete = show_machine()
    site = get_values_site()
    
    return render_template('add.html', station = station, machine_data = machine_data, slot = slot, edit_delete = edit_delete, site = site)

@app.route('/delete', methods=['GET', 'POST'])
@flask_login.login_required
def delete():
    return render_template('add.html')
        
@app.route('/logout')
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('index'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401
    
@app.route('/setup')
@flask_login.login_required
def setup():
    setup = setupMachine()
    return render_template('setup.html', setup = setup)

@app.route('/confirm_reject')
@flask_login.login_required
def confirm_reject():
    user_confirm = flask.request.form['confirm']
    user_reject = flask.request.form['reject']
    print(user_confirm)
    if request.args.get('confirm'):
        confirm_User(user_confirm)
        return render_template('index.html')
    if request.args.get('reject'):
        reject_User(user_reject)        
        return render_template('index.html')
    return render_template('index.html')

########################### End Function Login ###########################

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

@app.route('/trendDi')
def trendDi():
    return render_template('TrendDiwater.html')

@app.route('/status-carbon-resin')
def statusCR():
    return render_template('status-carbon-resin.html')



if __name__ == "__main__":
    app.run(debug=True)