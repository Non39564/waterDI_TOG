from fpdf import FPDF
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

@app.route('/dataapi', methods=["GET", "POST"])
def dataapi():
    url = requests.get("http://www.randomnumberapi.com/api/v1.0/random?min=0&max=25&count=10")
    text = url.text
    data = json.loads(text)
    user=[
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
        print(values_Site)
        Site = request.form.get(values_Site[0])
        Ip = request.form.get("Ip"+values_Site[0])
        Port = request.form.get("Port"+values_Site[0])
        Station = request.form.get("inputOP")
        Phase = request.form.get("Phase"+values_Site[0])
        Slot_Water = request.form.get("Slot_Water"+values_Site[0])
        Slot_Temp = request.form.get("Slot_Temp"+values_Site[0])
        if Slot_Water is None and Slot_Temp is None:
            edit = edit_machine_device(Site)
            Slot_Water = edit[0]['Slot_Water']
            Slot_Temp = edit[0]['Slot_Temp']
        print(Site, Ip, Port, Station, Phase, Slot_Water, Slot_Temp)
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
@flask_login.login_required
def setup():
    setup = setupMachine()
    show_machine = machine_DropDown_setup()
    return render_template('setup.html', setup = setup, show_machine = show_machine)

@app.route('/find_setup')
@flask_login.login_required
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
@flask_login.login_required
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

@app.route('/line')
def line():
    report = di_report()
    return render_template('line.html', report = report)

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
    return render_template('TrendDiwater.html', P4 = P4, P5 = P5, P9 = P9)

@app.route('/status-carbon-resin')
def statusCR():
    return render_template('status-carbon-resin.html')

@app.route('/download_alert')
def download_alert():
    report = error_report()
    pdf = FPDF("P", "mm", "A4")
    pdf.add_page()
    pdf.add_font('THSarabunNew', '', 'THSarabunNew.ttf', uni=True)
    
    page_width = pdf.w - 2 * pdf.l_margin

    pdf.set_font('THSarabunNew', '',14.0) 
    pdf.cell(page_width, 0.0, 'Alert Data', align='C')
    pdf.ln(10)
    
    pdf.set_font('THSarabunNew', '', 12)
    
    col_width = page_width/5
    
    pdf.ln(1)
    
    th = pdf.font_size*2

    pdf.set_fill_color(229, 229, 229)
    pdf.cell(col_width, th, str("Station"), 1, 0, 'C')
    pdf.cell(col_width, th, str("Phase"), 1, 0, 'C')
    pdf.cell(col_width, th, str("Machine"), 1, 0, 'C')
    pdf.cell(col_width, th, str("Detail"), 1, 0, 'C')
    pdf.cell(col_width, th, str("Date"), 1, 0, 'C')
    pdf.ln(th)
    
    for row in report:
        pdf.cell(col_width, th, str(row['Station']), border=1)
        pdf.cell(col_width, th, str(row['Phase']), border=1)
        pdf.cell(col_width, th, str(row['Site']), border=1)
        pdf.cell(col_width, th, str(row['Detail']), border=1)
        pdf.cell(col_width, th, str(row['Data']), border=1)
        pdf.ln(th)
        
    pdf.ln(10)
    
    pdf.set_font('THSarabunNew','',10.0) 
    pdf.cell(page_width, 0.0, '- end of report -', align='C')
    
    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers.set('Content-Disposition', 'attachment', filename="Alert Report" + '.pdf')
    response.headers.set('Content-Type', 'application/pdf')
    
    return response

@app.route('/download_Overview')
def download_Overview():
    report = di_report()
    pdf = FPDF("P", "mm", "A4")
    pdf.add_page()
    pdf.add_font('THSarabunNew', '', 'THSarabunNew.ttf', uni=True)
    
    page_width = pdf.w - 2 * pdf.l_margin

    pdf.set_font('THSarabunNew', '',14.0) 
    pdf.cell(page_width, 0.0, 'Deionized water Data', align='C')
    pdf.ln(10)
    
    pdf.set_font('THSarabunNew', '', 12)
    
    col_width = page_width/6
    
    pdf.ln(1)
    
    th = pdf.font_size*2

    pdf.set_fill_color(229, 229, 229)
    pdf.cell(col_width, th, str("Date"), 1, 0, 'C')
    pdf.cell(col_width, th, str("Phase"), 1, 0, 'C')
    pdf.cell(col_width, th, str("Machine"), 1, 0, 'C')
    pdf.cell(col_width, th, str("Status"), 1, 0, 'C')
    pdf.cell(col_width, th, str("DIWater"), 1, 0, 'C')
    pdf.cell(col_width, th, str("Temp"), 1, 0, 'C')
    pdf.ln(th)
    
    for row in report:
        if row["Water"] > 12:
            Status = "Pass"
        elif row["Water"] >= 10 and row["Water"] < 12:
            Status = "Monitor"
        else:
            Status = "Error"
        pdf.cell(col_width, th, str(row['Date']), border=1)
        pdf.cell(col_width, th, str(row['Phase']), border=1)
        pdf.cell(col_width, th, str(row['Site']), border=1)
        pdf.cell(col_width, th, str(Status), border=1)
        pdf.cell(col_width, th, str(row['Water']), border=1)
        pdf.cell(col_width, th, str(row['Temp']), border=1)
        pdf.ln(th)
        
    pdf.ln(10)
    
    pdf.set_font('THSarabunNew','',10.0) 
    pdf.cell(page_width, 0.0, '- end of report -', align='C')
    
    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers.set('Content-Disposition', 'attachment', filename="Alert Report" + '.pdf')
    response.headers.set('Content-Type', 'application/pdf')
    
    return response


if __name__ == "__main__":
    app.run(debug=True)