import socket
import time
import requests
from datetime import datetime


status = ''

def Frequency_check(data):
    if data >= 51:
        url = 'https://notify-api.line.me/api/notify'
        token = '4f8iOTmuyDB4lnQj8cFngHbL5VTVd5q3sbKXgUxSGLJ'
        headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
        msg = f"""
        แจ้งเตือนค่า Frequency ผิดปกติ
        ค่าที่วัดได้ { data }"""
        try:
            r = requests.post(url, headers=headers, data = {'message':msg})
            print(r.status_code)
        except:
            print('Line bot not working')


def line_bot(old,new):
    url = 'https://notify-api.line.me/api/notify'
    token = '4f8iOTmuyDB4lnQj8cFngHbL5VTVd5q3sbKXgUxSGLJ'
    headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
    msg = f"""
        รายงานแจ้งเตือนสถานะเครื่อง
        จากสถานะ { old }
        เปลี่ยนแปลงเป็น { new }"""
    try:
        r = requests.post(url, headers=headers, data = {'message':msg})
        print(r.status_code)
    except:
        print('Line bot not working')


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

while True:
        socket.setdefaulttimeout(.5)
        data = bytearray.fromhex("01030009003C95D9")
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = clientSocket.connect_ex(('10.3.55.130',32004))
        print(str('170.0.0.7')+" is Listening on Port "+ str(32004))
        clientSocket.send(data);
        dataFromServer = clientSocket.recv(1024);

        hex = dataFromServer.hex()
        fromhex = hex[6:-4]
        
        print()
        count = int(len(fromhex)/4)
        data = []
        num = 1
        for i in range(count):
            hexdata = fromhex[(num*4)-4:num*4]
            d = int(hexdata, base=16)
            data.append(d)
            num = num+1
            
        
        now = datetime.now()
        Timestamp = now.strftime("%Y-%m-%d %H:%M:%S") 
        dates,times = Timestamp.split(' ')

        newstatus = status_check(data[1])
        mode = mode_check(data[0])
        #Frequency_check(int(data[34])/100)
        if status != newstatus:
            #line_bot(status,newstatus)
            status = newstatus
            pass
        print(data)
        
        data_json = [
        {
            "Name": "Generator",
            "Status": status,
            "Mode": mode,
            "Frequency": int(data[34])/100,
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
        clientSocket.close()
        time.sleep(1)
