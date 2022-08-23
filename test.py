# def clean(phase, result):
#     if phase == 4:
#         data = 0
#     elif phase == 5:
#         data = 1
#     else :
#         data = 2
#     with open("./static/js/test.js", "r") as f:
#         lines = f.readlines()
#     with open("./static/js/test.js", "w") as f:
#         for line in lines:
#             if not f"""dataP{phase}.addRow([json[{data}].Data[{result}].id, json[{data}].Data[{result}].Water]);""" in line.strip("\n"):
#                 f.write(line)

#clean(5, 0)

# def checkdriver(phase, result):
#     if phase == "Phase 4":
#         phase = 4
#         data = 0
#     elif phase == "Phase 5":
#         phase = 5
#         data = 1
#     else :
#         phase = 9
#         data = 2
#     with open("./static/js/test.js", "r") as f:
#         lines = f.readlines()
#     with open("./static/js/test.js", "r") as f:
#         for line in lines:
#             print(phase)
#             print(data)
#             print(result)
#             if line.find(f"""dataP{phase}.addRow([json[{data}].Data[{result}].id, json[{data}].Data[{result}].Water]);""") != -1:
#                 print("Found!")
#                 break
#             else:
#                 print("Not found!")
   
# checkdriver("Phase 5", 0)  

# def addtoshow(phase, result ,Mname):
#     if phase == "Phase 4":
#         phase = 4
#         data = 0
#         line_insert_machine = 8
#         # more
#         line_push_machine = 70
#         line_push_shift = 105
#         line_add_data_Column = 114
#         line_add_data_Row = 119
#     elif phase == "Phase 5":
#         phase = 5
#         data = 1
#         line_insert_machine = 16
#         # more
#         line_push_machine = 78
#         line_push_shift = 105
#         line_add_data_Column = 134
#         line_add_data_Row = 134
#     else :
#         phase = 9
#         data = 2
#         line_insert_machine = 25
#         # more
#         line_push_machine = 87
#         line_push_shift = 105
#         line_add_data_Column = 145
#         line_add_data_Row = 150
#     # with open("./static/js/test.js", "r") as f:
#     #     lines = f.readlines()
#     # more
#     with open("./static/js/test.js", "r") as fl:
#         lines = fl.readlines()
#     # with open("./static/js/test.js", "w") as f:
#     #     lines[line_insert_machine] =  f'\n dataP{phase}.addRow([json[{data}].Data[{result}].id, json[{data}].Data[{result}].Water]);  \n'
#     #     a_file = open("./static/js/test.js", "w")
#     #     a_file.writelines(lines)
#     #     a_file.close()
#     # more
#     lines[line_insert_machine] =  f'\n dataP{phase}.addRow([json[{data}].Data[{result}].id, json[{data}].Data[{result}].Water]);  \n'
#     a_file_l = open("./static/js/test.js", "w")
#     a_file_l.writelines(lines)
#     a_file_l.close()
        
# addtoshow("Phase 9", 6)         

from multiprocessing import connection
from platform import machine
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
    
# def dynamicop():
#     op = []
#     connection = getConnection()
#     cursor = connection.cursor()
#     select_op = "select * from OP"
#     cursor.execute(select_op)
#     data = cursor.fetchall()
#     for row in range(len(data)):
#         op.append(data[row]["OP"])
#     return op
    
# def dynamicphase(op_id):
#     ph = []
#     connection = getConnection()
#     cursor = connection.cursor()
#     select_phase = "select * from phase where OP = '%s'" % (op_id)
#     cursor.execute(select_phase)
#     data = cursor.fetchall()
#     for row in range(len(data)):
#         ph.append(data[row]["Phase"])
#     return ph
        
# def get_dropdown_values():
#     op = dynamicop()
#     myDict = {}
#     for station in op:
    
#         key = station
#         op_id = station
        
#         dataphase = dynamicphase(op_id)
#         lst_p = []
#         for phase in dataphase:
#             if phase not in lst_p:
#                 lst_p.append( phase )
#         myDict[key] = lst_p
#         print(lst_p)
    
#     class_entry_relations = myDict
#     # print(class_entry_relations)
    
#     return class_entry_relations


# def dynamicmachine(machineid):
#     machine = []
#     connection = getConnection()
#     cursor = connection.cursor()
#     select_machine = """SELECT Machine.Machine, machine_station.Phase
#                         FROM Machine
#                         INNER JOIN machine_station ON Machine.ID=machine_station.ID 
#                         WHERE machine_station.Phase = '%s'""" % (machineid)
#     cursor.execute(select_machine)
#     data = cursor.fetchall()
#     for row in range(len(data)):
#         machine.append(data[row]["OP"])
#     print(machine)
#     return machine

# def dynamic_machine(phase):
#     machine = []
#     connection = getConnection()
#     cursor = connection.cursor()
#     select_machine = """SELECT machine.Machine, machine_station.Phase
#                         FROM machine
#                         INNER JOIN machine_station ON machine_station.ID=machine.ID and machine_station.Phase='%s'""" % (phase)
#     cursor.execute(select_machine)
#     data = cursor.fetchall()
#     for row in range(len(data)):
#         machine.append(data[row]["Machine"])
#     return machine
    
# def dynamic_phase_machine():
#     phase = []
#     connection = getConnection()
#     cursor = connection.cursor()
#     select_phase = "select * from Phase"
#     cursor.execute(select_phase)
#     data = cursor.fetchall()
#     for row in range(len(data)):
#         phase.append(data[row]["Phase"])
#     return phase    
    
# def get_dropdown_values_machine():
#     phase = dynamic_phase_machine()
#     myDict = {}
#     for station in phase:
    
#         key = station
#         phase = station
        
#         dataphase = dynamic_machine(phase)
#         lst_p = []
#         for phase in dataphase:
#             lst_p.append( phase )
#         myDict[key] = lst_p
    
#     class_entry_relations = myDict
#     print(class_entry_relations)
#     return class_entry_relations


# def dynamic_slot():
#     slot = []
#     connection = getConnection()
#     cursor = connection.cursor()
#     select_slot = "select * from Machine_Data"
#     cursor.execute(select_slot)
#     data = cursor.fetchall()
#     for row in range(len(data)):
#         slot.append(data[row]["Slot_Water"])
#         slot.append(data[row]["Slot_Temp"])
#     print(slot)
#     return slot   
    
# def show_machine():
#     connection = getConnection()
#     cursor = connection.cursor()
#     show_machine = """SELECT machine_master.Ip, 
#                             machine_master.Port,
#                             machine_station.Station, 
#                             machine_station.Phase,
#                             machine.Site,
#                             machine_data.Slot_Water,
#                             machine_data.Slot_Temp
#                         FROM machine_master
#                         INNER JOIN machine ON machine_master.Machine = machine.Machine
#                         INNER JOIN machine_station ON machine.ID = machine_station.ID
#                         INNER JOIN machine_data ON machine_data.Machine = machine_master.Machine"""
#     cursor.execute(show_machine)
#     data = cursor.fetchall()
#     for row in range(len(data)):
#         return data[row]
        
# def dynamic_phase_site():
#     phase = []
#     connection = getConnection()
#     cursor = connection.cursor()
#     select_phase = "select * from phase"
#     cursor.execute(select_phase)
#     data = cursor.fetchall()
#     for row in range(len(data)):
#         phase.append(data[row]["Phase"])
#     return phase
    
# def dynamic_site_phase(phase):
#     site = []
#     connection = getConnection()
#     cursor = connection.cursor()
#     select_site = "select * from phase where phase = '%s'" % (phase)
#     cursor.execute(select_site)
#     data = cursor.fetchall()
#     for row in range(len(data)):
#         site.append(data[row]["Site"])
#     return site
        
# def get_values_site():
#     phase = dynamic_phase_site()
#     myDict = {}
#     for site in phase:
    
#         key = site
#         phase_id = site
        
#         data_site = dynamic_site_phase(phase_id)
#         lst_p = []
#         for phase in data_site:
#             if phase not in lst_p:
#                 lst_p.append( phase )
#         myDict[key] = lst_p
    
#     class_entry_relations = myDict
#     print(class_entry_relations)
    
#     return class_entry_relations

# def find_users():
#     users = []
#     connection = getConnection()
#     cursor = connection.cursor()
#     find_users = "select * from user"
#     cursor.execute(find_users)
#     data = cursor.fetchall()
#     for row in range(len(data)):
#         users.append(data[row]["Username"])
#     return users

# def find_password(user):
#     password = []
#     connection = getConnection()
#     cursor = connection.cursor()
#     find_password = "select * from user where Username = '%s'" % (user)
#     cursor.execute(find_password)
#     data = cursor.fetchall()
#     for row in range(len(data)):
#         password.append(data[row]["Password"])
#     return password

# def users():
#     users = find_users()
#     myDict = {}
#     for username in users:
        
#         key = username
#         user = username
        
#         lst_p = {}
#         password = find_password(user)
#         for word in password:
#             # key = data[password]["Username"]
#             lst_p["password"] = (word)
#         myDict[key] = lst_p
#     class_entry_relations = myDict
#     print(class_entry_relations)

# def insert_Pre_User(username, Name, password):
#     connection = getConnection()
#     cursor = connection.cursor()
#     insert_Pre_User = "INSERT INTO pre_user VALUES ('%s','%s',PASSWORD('%s'))" % (username, Name, password)
#     cursor.execute(insert_Pre_User)
#     connection.commit()

# def show_recept():
#     connection = getConnection()
#     sql_recept = "SELECT Name from Pre_User"
#     cursor = connection.cursor()
#     cursor.execute(sql_recept)
#     user = cursor.fetchall()
#     return user
    
# def confirm_User(Name):
#     connection = getConnection()
#     cursor = connection.cursor()
#     add_pre_user = "INSERT INTO User SELECT Username, Name, Password FROM Pre_User WHERE Name='%s'" % (Name)
#     delete_pre_user = "DELETE FROM pre_user WHERE Name='%s'" % (Name)
#     cursor.execute(add_pre_user)
#     cursor.execute(delete_pre_user)
#     connection.commit()
        
# def reject_User(Name):
#     connection = getConnection()
#     cursor = connection.cursor()
#     delete_pre_user = "DELETE FROM pre_user WHERE Name='%s'" % (Name)
#     cursor.execute(delete_pre_user)
#     connection.commit()