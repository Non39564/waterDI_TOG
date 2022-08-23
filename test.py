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
