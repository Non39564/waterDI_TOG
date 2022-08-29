import pymysql

def getConnection():
    return pymysql.connect(
        host='localhost',
        db='water_di',
        user='root',
        password='',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
###################################### Line notify ######################################################
import requests
from datetime import datetime

now = datetime.now()
url = 'https://notify-api.line.me/api/notify'
token = '1ynH4ehbVZZK3ngffNqBjnZVdnU5gKtNIYLu14IOLD8'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

msg = """
รายงานแจ้งเตือนสถานะค่าแรงดัน 
ชื่อจุดติดตั้ง : PT-CW-250 RD.G13
สถานะแจ้งเตือน : High
ค่าแรงดันที่วัดได้ : 3.26 bar 
วันที่รายงาน : 29/08/2022
เวลาที่รายงาน : 08:18:11
ไม่ต่ำกว่า : 1.5 bar 
ไม่เกินกว่า : 3.25 bar"""
# r = requests.post(url, headers=headers, data = {'message':msg, 'name':"ชาวโลก"})
# print (r.text)
#############################################################################################################

def showerror():
    connection = getConnection()
    sql = """SELECT machine_station.Station, machine_station.Phase, machine_data.Site, di_error.Detail
            FROM machine_station
            JOIN machine ON machine_station.ID = machine.ID
            JOIN machine_data ON machine_data.Machine = machine.Machine
            JOIN di_error ON di_error.Site = machine_data.Site
            WHERE di_error.Data = CURDATE()"""
    cursor = connection.cursor()
    cursor.execute(sql)
    error = cursor.fetchall()
    for i in error:
        msg = f"""
รายงานแจ้งเตือนสถานะค่าน้ำ
ชื่อจุดติดตั้ง : {i["Site"]}
สถานะแจ้งเตือน : Check DB
ค่าแรงดันที่วัดได้ : Json Now
วันที่รายงาน : {now.strftime("%d/%m/%Y")}
เวลาที่รายงาน : {now.strftime("%H:%M:%S")}
ไม่ต่ำกว่า : data DB
ไม่เกินกว่า : data DB"""
        requests.post(url, headers=headers, data = {'message':msg})
    return error

def di_report():
    connection = getConnection()
    cursor = connection.cursor()
    di_report = "SELECT Date, Phase, Site, Water, Temp FROM di_report ORDER BY Date DESC, Time DESC"
    cursor.execute(di_report)
    data = cursor.fetchall()
    for i in data:
        if i["Water"] > 12:
            Status = "Pass"
        elif i["Water"] >= 10 and i["Water"] < 12:
            Status = "Monitor"
        else:
            Status = "Error"
        print(i)
        print(Status)
    # return data
    
di_report()