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
###################################### Line notifile ######################################################
import requests
url = 'https://notify-api.line.me/api/notify'
token = 'LOz6sHoZyt46LnvgQBKwpB0nY1q852OqznGnSAODvg0'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

msg = 'สาหวาดดีครับ'
#r = requests.post(url, headers=headers, data = {'message':msg})
#print (r.text)
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
        requests.post(url, headers=headers, data = {'message':i["Detail"]+" ที่ "+i["Site"]+" "+i["Station"]+" "+i["Phase"]})
        print()
    return error

showerror()