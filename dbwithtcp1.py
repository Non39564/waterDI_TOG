import json
from re import S
from pyModbusTCP.client import ModbusClient
import time
import requests
import pymysql
from datetime import datetime
from operator import itemgetter

#192.168.0.244
def getConnection ():
    return pymysql.connect(
        host = 'localhost',
        db = 'water_di',
        user = 'root',
        password = '',
        charset = 'utf8',
        cursorclass = pymysql.cursors.DictCursor
		)
    
def get_data(host,port):
    try:
        c = ModbusClient(host=host, port=port, unit_id=1, auto_open=True)
        rr = c.read_input_registers(0,28)
        l = []
        for i in range(0,28,2):
            if rr[i] == 65436 :
                rr[i] = -1 
            else:
                rr[i] = float(rr[i] / 100)
            l.append(rr[i])
        return l
    except:
        l = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        print(f"Post {port}  Host {host} is Error connecting")
        return l

    
def get_op_phase():
    oplist = []
    connection = getConnection()
    sql = "SELECT OP,Phase,Site FROM phase order by op,phase"
    cursor = connection.cursor()
    cursor.execute(sql)
    m = cursor.fetchall()
    for i in range(len(m)):
        op = m[i]['OP']
        phase = m[i]['Phase']
        ophase = op+'|'+phase

        if ophase not in oplist:
            oplist.append(op+"|"+phase)     
    return oplist

def get_offset_data():
    connection = getConnection()
    sql = "SELECT * from off_set"
    cursor = connection.cursor()
    cursor.execute(sql)
    off = cursor.fetchall()
    return off

def get_offset(Site,offset):
    pw,mw,pt,mt = 0,0,0,0
    for offset in offset:
        if Site == offset['Site']:
            pw = offset['Plus_Water']
            mw = offset['Minus_Water']
            pt = offset['Plus_Temp']
            mt =offset['Minus_Temp']
    return pw,mw,pt,mt

def line_bot_error_water(Site,status,data,date,time,min,max):
    url = 'https://notify-api.line.me/api/notify'
    token = '1ynH4ehbVZZK3ngffNqBjnZVdnU5gKtNIYLu14IOLD8'
    headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
    msg = f"""
    รายงานแจ้งเตือนสถานะค่าน้ำ DI 
    ชื่อจุดติดตั้ง : {Site}
    สถานะแจ้งเตือน : {status}
    ค่าน้ำที่วัดได้ : {data} 
    วันที่รายงาน : {date}
    เวลาที่รายงาน : {time}
    ไม่ต่ำกว่า : {min} 
    ไม่เกินกว่า : {max}"""
    r = requests.post(url, headers=headers, data = {'message':msg})
    if status == 'Normal':
        pass
    else:
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        connection = getConnection()
        sql = "INSERT INTO di_error(`Site`, `Detail`, `Date`) VALUES('%s','%s','%s')" % (Site,status,date)
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()

def line_bot_error_temp(Site,status,data,date,time,min,max):
    url = 'https://notify-api.line.me/api/notify'
    token = '1ynH4ehbVZZK3ngffNqBjnZVdnU5gKtNIYLu14IOLD8'
    headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
    msg = f"""
    รายงานแจ้งเตือนสถานะค่าอุณหภูมิ
    ชื่อจุดติดตั้ง : {Site}
    สถานะแจ้งเตือน : {status}
    ค่าอุณหภูมิที่วัดได้ : {data} 
    วันที่รายงาน : {date}
    เวลาที่รายงาน : {time}
    ไม่ต่ำกว่า : {min} 
    ไม่เกินกว่า : {max}"""
    r = requests.post(url, headers=headers, data = {'message':msg})
    if status == 'Normal':
        pass
    else:
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        connection = getConnection()
        sql = "INSERT INTO di_error(`Site`, `Detail`, `Date`) VALUES('%s','%s','%s')" % (Site,status,date)
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
    
def update_alarm(Site,data,type):
    connection = getConnection()
    if type == 'water':
        sql = "UPDATE off_set SET Status_Di = '%s' WHERE Site = '%s'" %(data,Site)
    if type == 'temp':
        sql = "UPDATE off_set SET Status_Temp = '%s' WHERE Site = '%s'" %(data,Site)
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    

    

def check_alarm(Site,data,date,time,min,max,type,Status_m):
    connection = getConnection()
    sql = "SELECT Site,Status_Di,Status_temp FROM off_set WHERE Site = '%s'" % (Site)
    cursor = connection.cursor()
    cursor.execute(sql)
    data_status = cursor.fetchall()
    for s in data_status:
        if type == 'water':
            
            if Status_m == s['Status_Di']:
                pass
            else:
                if Status_m == 'L':
                    line_bot_error_water(Site,"Low",data,date,time,min,max)
                    update_alarm(Site,'L','water')
                elif Status_m == 'N':
                    line_bot_error_water(Site,"Normal",data,date,time,min,max)
                    update_alarm(Site,'N','water')
                elif Status_m == 'H':
                    line_bot_error_water(Site,"High",data,date,time,min,max) 
                    update_alarm(Site,'H','water')
           
        elif type == 'temp':
            if s['Status_temp'] == Status_m:
                pass
            else:
                if Status_m == 'L':
                    line_bot_error_temp(Site,"Low",data,date,time,min,max)
                    update_alarm(Site,'L','temp') 
                elif Status_m == 'N':
                    line_bot_error_temp(Site,"Normal",data,date,time,min,max)
                    update_alarm(Site,'N','temp') 
                elif Status_m == 'H':
                    line_bot_error_temp(Site,"High",data,date,time,min,max)
                    update_alarm(Site,'H','temp') 


def Normal_check(Site,data,date,time,min,max,type):
    connection = getConnection()
    sql = "SELECT Site,Status_Di,Status_temp FROM off_set WHERE Site = '%s'" % (Site)
    cursor = connection.cursor()
    cursor.execute(sql)
    data_status = cursor.fetchall()
    for status in data_status:
        if type == 'water':
            if status['Status_Di'] == 'L' or status['Status_Di'] == 'H':
                line_bot_error_water(Site,"Normal",data,date,time,min,max)
        elif type == 'temp':
            if status['Status_temp'] == 'L' or status['Status_temp'] == 'H':
                line_bot_error_temp(Site,"Normal",data,date,time,min,max)

            
              
def water_check(Site,min,max,water,date,time):
    if water > max:
        check_alarm(Site,water,date,time,min,max,'water','H')
    elif water < min:
        check_alarm(Site,water,date,time,min,max,'water','L')
    else:
        Normal_check(Site,water,date,time,min,max,'water')
        update_alarm(Site,'N','water')

def temp_check(Site,min,max,temp,date,time):
    if temp > max:
        check_alarm(Site,temp,date,time,min,max,'temp','H')
    elif temp < min:
        check_alarm(Site,temp,date,time,min,max,'temp','L')
    else:
        Normal_check(Site,temp,date,time,min,max,'temp')       
        update_alarm(Site,'N','temp')
        

                

def Alarm(Site,offset,water,temp):
    now = datetime.now()
    Timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
    date,time = Timestamp.split(" ")
    for os in offset:
        if Site == os['Site']:
            minw = os['Low_Water']
            maxw = os['Hight_Water']
            mint = os['Low_Temp']
            maxt = os['Hight_Temp']
            water_check(Site,minw,maxw,water,date,time)
            temp_check(Site,mint,maxt,temp,date,time)
                
              
                
def insert_report(Station,Phase,Site,Temp,Water):
    now = datetime.now()
    insert_time = now.strftime("%Y-%m-%d %H:00:00")
    d,t = insert_time.split(" ")
    connection = getConnection()
    sql = "INSERT INTO di_report(`Station`, `Phase`, `Site`, `Temp`, `Water`,`Date`,`Time`) VALUES('%s','%s','%s','%s','%s','%s','%s')" % (Station,Phase,Site,Temp,Water,d,t)
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
            
            
set_time = ""
dataexport = []
times = 0
save = False

while True:
    now = datetime.now()
    Timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    d,t = Timestamp.split(" ")
    
    offset = get_offset_data()
    ti = now.strftime("%H")
    print(times)
    if ti != times:
        times = ti
        save = True
    
    ip_port = []
    data = []
    report = []
    connection = getConnection()
    sql = "SELECT * FROM machine_master"
    cursor = connection.cursor()
    cursor.execute(sql)
    m = cursor.fetchall()
    
    for i in m:
        if i['Ip']+":"+str(i['Port']) not in ip_port:
            ip_port.append(i['Ip']+":"+str(i['Port']))
    for j in range(len(ip_port)):
        port,host = ip_port[j].split(":")
        data.append(get_data(str(port),int(host)))
    
    
    oplist= get_op_phase()
    for o in range(len(oplist)):
        op,phase = oplist[o].split("|")
        lists = {"Station":op,"Phase":phase,"Data":[],"Date":d,"Time":t}
        connection = getConnection()
        sql= f"""
        SELECT p.OP as OP,p.Phase as phase ,p.Site as Site, mm.Ip as Ip, mm.Port as Port, md.Slot_Temp as Slot_Temp ,md.Slot_Water as Slot_Water 
        FROM machine_data as md,machine_master as mm, phase as p 
        WHERE p.Site = md.Site AND md.Machine = mm.Machine AND p.OP = '{op}' and p.Phase = '{phase}'
        """
        cursor = connection.cursor()
        cursor.execute(sql)
        re = cursor.fetchall()
        if len(re) > 0:
            # ip port site op phase
            for m in re:
                for k in range(len(ip_port)):
                    if m['Ip']+":"+str(m['Port']) == ip_port[k]:
                        pw,mw,pt,mt = get_offset(m['Site'],offset)
                        water_data = (data[k][m['Slot_Water']-1] + pw) - mw
                        temp_data = (data[k][m['Slot_Temp']-1] + pt) - mt
                        
                        water_data = round(water_data, 2)
                        temp_data = round(temp_data, 2)
                            
                        if water_data == -1 and temp_data == -1:
                            pass
                        elif water_data == -1 and temp_data !=-1:
                            water_data = -999
                            dicts = {"id":m['Site'],"Water":water_data,"Temp":temp_data}
                            lists['Data'].append(dicts)
                        else:
                            if save is True:
                                insert_report(m['OP'],m['phase'],m['Site'],temp_data,water_data)
                            Alarm(m['Site'],offset,water_data,temp_data)
                            dicts = {"id":m['Site'],"Water":water_data,"Temp":temp_data}
                            lists['Data'].append(dicts)
                        
                  
            report.append(lists)     
       
    num = []
    for i in range(len(report)):
        num.append(report[i]['Phase'])
    if 'Phase 4' not in num:
        report.append({"Station": "OP2", "Phase": "Phase 4", "Data":[],"Date": d,"Time": t})
        num.append('Phase 4')
    if 'Phase 5' not in num:
        report.append({"Station": "OP2", "Phase": "Phase 5", "Data":[],"Date": d,"Time": t})
        num.append('Phase 5')
    if 'Phase 9' not in num:
        report.append({"Station": "OP2", "Phase": "Phase 9", "Data":[],"Date": d,"Time": t})
        num.append('Phase 9')  
        
    newlist = sorted(report, key=itemgetter('Phase'))
    print(newlist)  
    if save is True:
        save = False
    try:
        url = "http://10.3.9.156/postdata"
        x = requests.post(url, json=newlist)
        print(x.status_code)
    except:
        print("Don't send to server")
    print()          
    time.sleep(1)

