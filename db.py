import pymysql

########################### Function DB ###########################

def getConnection():
    return pymysql.connect(
        host='localhost',
        db='water_di',
        user='root',
        password='',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    
def showerror():
    connection = getConnection()
    sql = """SELECT machine_station.Station, machine_station.Phase, di_error.Detail
            FROM machine_station
            JOIN machine ON machine_station.ID=machine_station.ID
            JOIN machine_data ON Machine.Machine=machine_data.Machine
            JOIN di_error ON di_error.Site=machine_data.Site"""
    cursor = connection.cursor()
    cursor.execute(sql)
    error = cursor.fetchall()
    return error

def show_recept():
    connection = getConnection()
    sql_recept = "SELECT Name from Pre_User"
    cursor = connection.cursor()
    cursor.execute(sql_recept)
    user = cursor.fetchall()
    return user

def Add_Machine(Machine, IP, PORT, Station, Phase):
    connection = getConnection()
    insert_Machine_Master = "INSERT INTO Machine_Master(Machine, Ip, Port) VALUES('%s', '%s', '%s')" % (Machine, IP, PORT)
    insert_Machine_Station = "INSERT INTO Machine_Station(Station, Phase) VALUES('%s', '%s')" % (Station, Phase)
    insert_Machine = "INSERT INTO Machine(Machine) VALUES('%s')" % (Machine)
    cursor = connection.cursor()
    cursor.execute(insert_Machine_Master)
    cursor.execute(insert_Machine_Station)
    cursor.execute(insert_Machine)
    connection.commit()

def Add_Device(Machine, Site, Slot_Temp, Slot_Water):
    connection = getConnection()
    cursor = connection.cursor()
    update_Machine = "UPDATE machine SET Site='%s' WHERE Machine = '%s'" % (Site, Machine)
    insert_Machine_Data = "INSERT INTO Machine_Data(Site, Machine, Slot_Temp, Slot_Water) VALUES('%s', '%s', '%s', '%s')" % (Site, Machine, Slot_Temp, Slot_Water)
    cursor.execute(update_Machine)
    cursor.execute(insert_Machine_Data)
    connection.commit()
    
def Di_error(Machine, Detail, Date):
    connection = getConnection()
    insert_error = "INSERT INTO DI_Error(Machine, Detail, Date) VALUES('%s', '%s', '%s')" % (Machine, Detail, Date)
    cursor = connection.cursor()
    cursor.execute(insert_error)
    connection.commit()
    
def DI_Report(Station, Phase, Site, Temp, Water, Date, Time, TimeStamp):
    connection = getConnection()
    insert_report = """INSERT INTO DI_Report(Station, Phase, Site, Temp, Water, Date, Time, TimeStamp) 
                        VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % (Station, Phase, Site, Temp, Water, Date, Time, TimeStamp)
    cursor = connection.cursor()
    cursor.execute(insert_report)
    connection.commit()
    
def log_status(Machine, Status, Datetime):
    connection = getConnection()
    insert_error = "INSERT INTO Log_Status(Machine, Status, DateTime) VALUES('%s', '%s', '%s')" % (Machine, Status, Datetime)
    cursor = connection.cursor()
    cursor.execute(insert_error)
    connection.commit()
    
def add_phase(OP, Phase, Site):
    op = []
    OP = "OP"+str(OP)
    Phase = "Phase "+str(Phase)
    connection = getConnection()
    cursor = connection.cursor()
    select_op = "select * from OP"
    cursor.execute(select_op)
    data = cursor.fetchall()
    for row in data:
        op.append(row["OP"])
    if OP in op:
        insert_site = "INSERT INTO Off_Set VALUES('%s', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)" % (Site)
        insert_phase = "INSERT INTO Phase(OP, Phase, Site) VALUES('%s', '%s', '%s')" % (OP, Phase, Site)
        cursor.execute(insert_site)
        cursor.execute(insert_phase)
        connection.commit()
    else:
        insert_site = "INSERT INTO Off_Set VALUES('%s', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)" % (Site)
        insert_op = "INSERT INTO OP(OP) VALUES('%s')" % (OP)
        insert_phase = "INSERT INTO Phase(OP, Phase, Site) VALUES('%s', '%s', '%s')" % (OP, Phase, Site)
        cursor.execute(insert_site)
        cursor.execute(insert_op)
        cursor.execute(insert_phase)
        connection.commit()
        
def dynamicop():
    op = []
    connection = getConnection()
    cursor = connection.cursor()
    select_op = "select * from OP"
    cursor.execute(select_op)
    data = cursor.fetchall()
    for row in range(len(data)):
        op.append(data[row]["OP"])
    return op
    
def dynamicphase(op_id):
    ph = []
    connection = getConnection()
    cursor = connection.cursor()
    select_phase = "select * from phase where OP = '%s'" % (op_id)
    cursor.execute(select_phase)
    data = cursor.fetchall()
    for row in range(len(data)):
        ph.append(data[row]["Phase"])
    return ph
        
def get_dropdown_values():
    op = dynamicop()
    myDict = {}
    for station in op:
    
        key = station
        op_id = station
        
        dataphase = dynamicphase(op_id)
        lst_p = []
        for phase in dataphase:
            if phase not in lst_p:
                lst_p.append( phase )
        myDict[key] = lst_p
    
    class_entry_relations = myDict
    return class_entry_relations

def dynamic_machine(phase):
    machine = []
    connection = getConnection()
    cursor = connection.cursor()
    select_machine = """SELECT machine.Machine, machine_station.Phase
                        FROM machine
                        INNER JOIN machine_station ON machine_station.ID=machine.ID and machine_station.Phase='%s'""" % (phase)
    cursor.execute(select_machine)
    data = cursor.fetchall()
    for row in range(len(data)):
        machine.append(data[row]["Machine"])
    return machine
    
def dynamic_phase_machine():
    phase = []
    connection = getConnection()
    cursor = connection.cursor()
    select_phase = "select * from Phase"
    cursor.execute(select_phase)
    data = cursor.fetchall()
    for row in range(len(data)):
        phase.append(data[row]["Phase"])
    return phase    
    
def get_dropdown_values_machine():
    phase = dynamic_phase_machine()
    myDict = {}
    for station in phase:
    
        key = station
        phase = station
        
        dataphase = dynamic_machine(phase)
        lst_p = []
        for phase in dataphase:
            lst_p.append( phase )
        # print(key)
        myDict[key] = lst_p
    
    class_entry_relations = myDict
    return class_entry_relations

def dynamic_slot():
    slot = []
    myDict = {}
    connection = getConnection()
    cursor = connection.cursor()
    select_slot = "select * from Machine_Data"
    cursor.execute(select_slot)
    data = cursor.fetchall()
    for row in range(len(data)):
        slot.append(data[row]["Slot_Water"])
        slot.append(data[row]["Slot_Temp"])
    for all_slot in slot:
        myDict[all_slot] = all_slot
    
    class_entry_relations = myDict
    return class_entry_relations

def show_machine():
    connection = getConnection()
    cursor = connection.cursor()
    show_machine = """SELECT machine_master.Ip, 
                            machine_master.Port,
                            machine_station.Station, 
                            machine_station.Phase,
                            machine_data.Slot_Water,
                            machine_data.Slot_Temp
                        FROM machine_master
                        INNER JOIN machine ON machine_master.Machine = machine.Machine
                        INNER JOIN machine_station ON machine.ID = machine_station.ID
                        INNER JOIN machine_data ON machine_data.Machine = machine_master.Machine"""
    cursor.execute(show_machine)
    data = cursor.fetchall()
    return data

def setupMachine():
    connection = getConnection()
    cursor = connection.cursor()
    show_setup = """SELECT off_set.Site, off_set.Low_Water, off_set.Hight_Water, off_set.Plus_Water, off_set.Minus_Water, 
                    off_set.Low_Temp, off_set.Hight_Temp, off_set.Plus_Temp, off_set.Minus_Temp
                     FROM off_set"""
    cursor.execute(show_setup)
    data = cursor.fetchall()
    return data

def dynamic_phase_site():
    phase = []
    connection = getConnection()
    cursor = connection.cursor()
    select_phase = "select * from phase"
    cursor.execute(select_phase)
    data = cursor.fetchall()
    for row in range(len(data)):
        phase.append(data[row]["Phase"])
    return phase
    
def dynamic_site_phase(phase):
    site = []
    connection = getConnection()
    cursor = connection.cursor()
    select_site = "select * from phase where phase = '%s'" % (phase)
    cursor.execute(select_site)
    data = cursor.fetchall()
    for row in range(len(data)):
        site.append(data[row]["Site"])
    return site
        
def get_values_site():
    phase = dynamic_phase_site()
    myDict = {}
    for site in phase:
    
        key = site
        phase_id = site
        
        data_site = dynamic_site_phase(phase_id)
        lst_p = []
        for phase in data_site:
            if phase not in lst_p:
                lst_p.append( phase )
        myDict[key] = lst_p
    
    class_entry_relations = myDict
    print(class_entry_relations)
    
    return class_entry_relations

def find_users():
    users = []
    connection = getConnection()
    cursor = connection.cursor()
    find_users = "select * from user"
    cursor.execute(find_users)
    data = cursor.fetchall()
    for row in range(len(data)):
        users.append(data[row]["Username"])
    return users

def find_password(user):
    password = []
    connection = getConnection()
    cursor = connection.cursor()
    find_password = "select * from user where Username = '%s'" % (user)
    cursor.execute(find_password)
    data = cursor.fetchall()
    for row in range(len(data)):
        password.append(data[row]["Password"])
    return password

def users():
    users = find_users()
    myDict = {}
    for username in users:
        
        key = username
        user = username
        
        lst_p = {}
        password = find_password(user)
        for word in password:
            lst_p["password"] = (word)
        myDict[key] = lst_p
    class_entry_relations = myDict
    return class_entry_relations

def insert_Pre_User(username, Name, password):
    connection = getConnection()
    cursor = connection.cursor()
    insert_Pre_User = "INSERT INTO pre_user VALUES ('%s','%s',PASSWORD('%s'))" % (username, Name, password)
    cursor.execute(insert_Pre_User)
    connection.commit()
    
def confirm_User(Name):
    connection = getConnection()
    cursor = connection.cursor()
    add_pre_user = "INSERT INTO User SELECT Username, Name, Password FROM Pre_User WHERE Name='%s'" % (Name)
    delete_pre_user = "DELETE FROM pre_user WHERE Name='%s'" % (Name)
    cursor.execute(add_pre_user)
    cursor.execute(delete_pre_user)
    connection.commit()
        
def reject_User(Name):
    connection = getConnection()
    cursor = connection.cursor()
    delete_pre_user = "DELETE FROM pre_user WHERE Name='%s'" % (Name)
    cursor.execute(delete_pre_user)
    connection.commit()

########################### End Function DB ###########################
