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
