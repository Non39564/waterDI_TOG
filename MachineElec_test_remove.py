import socket
import time
import requests
from datetime import datetime
from pymongo import MongoClient

def get_data():
    try:
        socket.setdefaulttimeout(.5)
        data = bytearray.fromhex("01030009003C95D9")
        
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = clientSocket.connect_ex(('10.3.55.130',32004))
        print(str('170.0.0.7')+" is Listening on Port "+ str(32004))
        clientSocket.send(data)
        dataFromServer = clientSocket.recv(1024)

        hex = dataFromServer.hex()
        fromhex = hex[6:-4]
        count = int(len(fromhex)/4)
        data = []
        num = 1
        for i in range(count):
            hexdata = fromhex[(num*4)-4:num*4]
            d = int(hexdata, base=16)
            data.append(d)
            num = num+1
        clientSocket.close()
        return data
    except Exception as e:
        print(e)
        return []
        
def status_check(data):
    if data == 0:
        return 'Off'
    elif data == 1:
        return 'Stop'
    elif data == 2:
        return 'Preheat'
    elif data == 3:
        return 'Precrank'
    elif data == 4:
        return 'Crank'
    elif data == 5:
        return 'Starter Disconnect'
    elif data == 6:
        return 'PreRamp'
    elif data == 7:
        return 'Ramp'
    elif data == 8:
        return 'Running'
    elif data == 9:
        return 'Fault Shutdown'
    elif data == 10:
        return 'Prerun Setup'
    elif data == 11:
        return 'Runtime Setup'
    elif data == 12:
        return 'Factory Test'
    elif data == 13:
        return 'Waiting For Powerdown'

def mode_check(mode):
    if mode == 0:
        return 'Off'
    elif mode == 1:
        return 'Auto'
    elif mode == 2:
        return 'Manual'

def Frequency_check(data): 
    if 0 < data <= 50:
        url = 'https://notify-api.line.me/api/notify'
        #token = 'OPrQKKMqvD0trSpGBWzjBwWpLGPFGMHS8r2LtEXHSp1'
        token = 'SVxAXLRwuSkx9VC0hKF7ciCD1vMlPBiPUW9EihAMZWV'
        headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
        msg = f"""
แจ้งเตือนค่า Frequency ผิดปกติ
ค่าที่วัดได้ { data }"""
        try:
            r = requests.post(url, headers=headers, data = {'message':msg})
            print(r.status_code)
        except:
            print('Line bot not working')

def line_bot(old,new, mas, l1v,l1a,l2v,l2a,l3v,l3a, frequency):
    if old != '':
        url = 'https://notify-api.line.me/api/notify'
        #token = 'OPrQKKMqvD0trSpGBWzjBwWpLGPFGMHS8r2LtEXHSp1'
        token = 'SVxAXLRwuSkx9VC0hKF7ciCD1vMlPBiPUW9EihAMZWV'
        headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
        if mas == 'mode':
            msg = f"""
รายงานแจ้งเตือนสถานะเครื่อง
โหมดก่อนหน้า { old }
โหมดที่เปลี่ยนแปลง { new }
ค่า Frequency : {frequency}
ค่า L1 : {l1v}  ,  {l1a}
ค่า L2 : {l2v}  ,  {l2a}
ค่า L3 : {l3v}  ,  {l3a}"""
        elif mas == 'staus':
            msg = f"""
รายงานแจ้งเตือนสถานะเครื่อง
จากสถานะ { old }
เปลี่ยนแปลงเป็น { new }"""
        try:
            r = requests.post(url, headers=headers, data = {'message':msg})
            print(r.status_code)
        except:
            print('Line bot not working')
    else:
        pass

def line_bot_running(l1v,l1a,l2v,l2a,l3v,l3a, frequency):
    url = 'https://notify-api.line.me/api/notify'
    #token = 'OPrQKKMqvD0trSpGBWzjBwWpLGPFGMHS8r2LtEXHSp1'
    token = 'SVxAXLRwuSkx9VC0hKF7ciCD1vMlPBiPUW9EihAMZWV'

    headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
    msg = f"""
รายงานแจ้งเตือนสถานะเครื่อง
โหมด Running
ค่า Frequency : {frequency}
ค่า L1 : {l1v}  ,  {l1a}
ค่า L2 : {l2v}  ,  {l2a}
ค่า L3 : {l3v}  ,  {l3a}"""
    try:
        r = requests.post(url, headers=headers, data = {'message':msg})
        print(r.status_code)
    except:
        print('Line bot not working')
    

mode_defalt = ''
status_defalt = ''

while True:
    data = get_data()
    newstatus = status_check(data[1])
    mode = mode_check(data[0])
    now = datetime.now()
    
    if status_defalt != newstatus:
        print('chacge status to '+newstatus)
        line_bot(status_defalt,newstatus,'status', data[8],data[12],data[9],data[13],data[10],data[14], int(data[34])/100)
        status_defalt = newstatus
        
    if mode_defalt != mode:
        print('chacge mode to '+mode)
        line_bot(mode_defalt,mode,'mode', data[8],data[12],data[9],data[13],data[10],data[14], int(data[34])/100)
        mode_defalt = mode
        
    if mode == 'Running':
        Frequency_check(int(data[34])/100)
            
    Timestamp = now.strftime("%Y-%m-%d %H:%M:%S") 
    dates,times = Timestamp.split(' ')
    
    data_json = [
        {
            "Name": "Generator",
            "Status": newstatus,
            "Mode": mode,
            "Frequency": int(data[34])/100,
            "AverageEngineSpeed": int(data[58])*0.125,
            "Coolant Temp" : round(((int(data[54])/10) - 32) * (5/9),2),
            "Speed": 0,
            "Power (A)": [
                {
                    "L1": data[12],
                    "L2": data[13],
                    "L3": data[14],
                    "Total": 0
                    }
                ],
            "Power (V)": [
                {
                    "L1": data[8],
                    "L2": data[9],
                    "L3": data[10],
                    "Total": 0
                    }
                ],
            "Date": dates,
            "Time": times
            }
        ]  
    print(data_json)
    
    try:
        url = "http://10.3.9.156:80/postdata_generator"
        x = requests.post(url, json=data_json)
        print(x.status_code)  
    except:
        print("Don't send data")  
        num = 0
    client = MongoClient('localhost',27017,serverSelectionTimeoutMS=1500)
    db = client.Generator_Elec
    tb = db['report']
    tb.insert_many(data_json)
    print('insert to mogodb')
    print()
    time.sleep(5)