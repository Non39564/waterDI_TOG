from fpdf import FPDF
import os
import sys
from flask import Flask, make_response, jsonify, request, Response
from flask_login import LoginManager
import flask_login, flask
import json, requests
from flask import render_template as real_render_template
from functools import partial
from db import *
from datetime import datetime
from pymongo import MongoClient


app = Flask(__name__)
    
app.secret_key = 'waterdishow'

error = showerror()
user_recept = show_recept()
render_template = partial(real_render_template, error=error, user_recept=user_recept)



dataexport = 0

@app.route('/postdata', methods=["GET", "POST"])
def postdata():
    if request.method == 'POST':
        print("post")
        data = request.json
        now = datetime.now()
        sec = now.strftime("%S")
        json_object = json.dumps(data)
        with open("data.json", "w") as outfile:
            outfile.write(json_object)
        
        if int(sec) % 10 == 0 :
            client = MongoClient('localhost',27017)
            db = client.Water_di
            tb = db['report']
            tb.insert_many(data)
            print('insert to mogodb')
            dataexport = 0


        return "postdata succress"

@app.route('/dataapi', methods=["GET", "POST"])
def dataapi():
    js = open('data.json')
    data = json.load(js) 
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return jsonify(data)

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
    Site = request.args.get('Site')
    delete_device(Site)
    return flask.redirect(flask.url_for('addmachine'))

@app.route('/edit', methods=['GET', 'POST'])
@flask_login.login_required
def edit():
    Site = request.args.get('edit')
    edit = edit_machine_device(Site)
    station = get_dropdown_values()
    slot = dynamic_slot()
    return render_template('edit_device.html', edit = edit, station = station, slot = slot)

@app.route('/blank')
@flask_login.login_required
def blank():
    return render_template('blank.html')

@app.route('/edit_value', methods=['GET', 'POST'])
@flask_login.login_required
def edit_value():
    if request.method == 'POST':
        result = request.form.to_dict()
        values = result.values()
        values_Site = list(values)
        Site = request.form.get(values_Site[0])
        Ip = request.form.get("Ip"+values_Site[0])
        Port = request.form.get("Port"+values_Site[0])
        Station = request.form.get("inputOP")
        Phase = request.form.get("Phase"+values_Site[0])
        Slot_Water = request.form.get("Slot_Water"+values_Site[0])
        Slot_Temp = request.form.get("Slot_Temp"+values_Site[0])
        if Slot_Water is None and Slot_Temp is None:
            edit = edit_machine_device(values_Site[0])
            print(Site)
            Slot_Water = edit[0]['Slot_Water']
            Slot_Temp = edit[0]['Slot_Temp']
        edit_device(Ip, Port, Station, Phase, Slot_Water, Slot_Temp, Site)
    return flask.redirect(flask.url_for('blank'))
        
@app.route('/logout')
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('index'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401
    
@app.route('/setup')
# @flask_login.login_required
def setup():
    setup = setupMachine()
    show_machine = machine_DropDown_setup()
    return render_template('setup.html', setup = setup, show_machine = show_machine)

@app.route('/find_setup')
# @flask_login.login_required
def find_setup():
    selectionMachine = request.args.get('selectionMachine')
    setup = show_site_machine(selectionMachine)
    show_machine = machine_DropDown_setup()
    return render_template('setup.html', setup = setup, show_machine = show_machine, selectionMachine=selectionMachine)

@app.route('/confirm_reject', methods=['GET', 'POST'])
@flask_login.login_required
def confirm_reject():
    if request.args.get('confirm'):
        user_confirm = request.args.get('confirm')
        confirm_User(user_confirm)
        return flask.redirect(flask.url_for('index'))
    if request.args.get('reject'):
        user_reject = request.args.get('reject')
        reject_User(user_reject)        
        return flask.redirect(flask.url_for('index'))
    return flask.redirect(flask.url_for('index'))

@app.route('/change_setup' , methods=['GET', 'POST'])
# @flask_login.login_required
def change_setup():
    setup = setupMachine()
    name_site = []
    for i in setup:
        name_site.append(i['Site'])
    for j in range(len(name_site)):
        site = request.args.get(f'{name_site[j]}')
        low_water = request.args.get(f'Low_Water_{name_site[j]}')
        high_water = request.args.get(f'High_Water_{name_site[j]}')
        plus_water = request.args.get(f'Plus_Water_{name_site[j]}')
        minus_water = request.args.get(f'Minus_Water_{name_site[j]}')
        plus_temp = request.args.get(f'Plus_Temp_{name_site[j]}')
        minus_temp = request.args.get(f'Minus_Temp_{name_site[j]}')
        update_setup(site, low_water, high_water, plus_water, minus_water, plus_temp, minus_temp)
    return flask.redirect(flask.url_for('setup'))

########################### End Function Login ###########################

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/line', methods=['GET', 'POST'])
def line():
    if request.method == 'POST':
        if request.values["selection_day"] != "0":
            day = flask.request.form['selection_day']
            month = flask.request.form['selection_month']
            year = flask.request.form['year']
            report = di_report_custom_day(day, month, year)
            table = report_line_day(day, month ,year)
            column = somlinecolumn()
            customday = "True"
            return render_template('line.html', report = report, table = table, column = column, customday = customday)
        month = flask.request.form['selection_month']
        year = flask.request.form['year']
        report = di_report_custom(month, year)
        table = report_line_month(month ,year)
        column = somlinecolumn()
        custom = "True"
        return render_template('line.html', report = report, table = table, column = column, custom = custom)
    report = di_report_now()
    table = reportsomline()
    column = somlinecolumn()
    now = "True"
    return render_template('line.html', report = report, table = table, column = column, now = now)

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/alert')
def alert():
    report = error_report()
    return render_template('alert.html', report = report)

@app.route('/trendDi')
def trendDi():
    P4 = trend_DI_P4()
    P5 = trend_DI_P5()
    P9 = trend_DI_P9()
    print(P4)
    return render_template('TrendDiwater.html', P4 = P4, P5 = P5, P9 = P9)

@app.route('/trendDi-chart')
def trendDiChart():
    P4 = trend_DI_P4()
    P5 = trend_DI_P5()
    P9 = trend_DI_P9()
    print(P4)
    return render_template('trend-di-chart.html', P4 = P4, P5 = P5, P9 = P9)

@app.route('/status-carbon-resin')
def statusCR():
    return render_template('status-carbon-resin.html')

@app.route("/data_line", methods=["POST","GET"])
def data_line():
    
    if request.method == 'POST':
        draw = request.form['draw'] 
        row = int(request.form['start'])
        rowperpage = int(request.form['length'])
        searchValue = request.form["search[value]"]
        
        report = di_report_now()
        totalRecords = len(report)
        
        likeString = "%" + searchValue +"%"
        filter = di_report_filter_table(likeString)
        totalRecordwithFilter = len(filter)

        if searchValue == '':
            report = di_report_limit(row, rowperpage)
        else:
            report = di_report_filter_table_limit(likeString,row, rowperpage)
        data = []
        print(totalRecordwithFilter)
        for d in report:
            data.append({
                'Status': d['State'],
                'Phase': d['Phase'],
                'Site': d['Site'],
                'DIWater': d['Water'],
                'Date': d['Date'],
                'Time': str(d['Time']),
                'Temp':d['Temp']
            })
        response = {
                'draw': draw,
                'iTotalRecords': totalRecords,
                'iTotalDisplayRecords': totalRecordwithFilter,
                'aaData': data,
            }
        return jsonify(response)

@app.route("/data_alert", methods=["POST","GET"])
def data_alert():
    
    if request.method == 'POST':
        draw = request.form['draw'] 
        row = int(request.form['start'])
        rowperpage = int(request.form['length'])
        searchValue = request.form["search[value]"]
        
        report = error_report()
        totalRecords = len(report)
        
        likeString = "%" + searchValue +"%"
        filter = filter_table(likeString)
        totalRecordwithFilter = len(filter)
        
        if searchValue == '':
            report = error_report_limit(row, rowperpage)
        else:
            report = filter_table_limit(likeString,row, rowperpage)
          
        data = []
        for d in report:
            data.append({
                'Station': d['Station'],
                'Phase': d['Phase'],
                'Site': d['Site'],
                'Detail': d['Detail'],
                'Date': d['Date'],
                'Time': str(d['Time'])
            })
        print(data)
        response = {
                'draw': draw,
                'iTotalRecords': totalRecords,
                'iTotalDisplayRecords': totalRecordwithFilter,
                'aaData': data,
            }
        return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, host='10.3.9.156' ,port=80)