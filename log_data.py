from pyModbusTCP.client import ModbusClient
import time
from pymongo import MongoClient
from datetime import datetime

while True:
    l = []
    try:
        c = ModbusClient(host='10.3.55.131', port=502, unit_id=1, auto_open=True)
        rr = c.read_input_registers(0,28)
        l = []
        for i in range(0,28,2):
            if rr[i] == 65436 :
                rr[i] = -1 
            else:
                rr[i] = float(rr[i] / 100)
            l.append(rr[i])
    except:
        l = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        print(f"Post 10.3.55.131  Host 502 is Error connecting")
    print(l)
    
    now = datetime.now()
    sec = now.strftime("%H:%M:%S")
    client = MongoClient('localhost',27017)
    db = client.Water_di
    tb = db['HC-5 station 1']
    tb.insert_one(
        {'Machine': 'HC-5 Station 1',
         'time': sec,
         'water': l[2],
         'temp': l[3]
         })
    time.sleep(1)
