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
    print(class_entry_relations)
    return class_entry_relations
dynamic_slot()