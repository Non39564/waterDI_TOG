import pymysql, base64, itertools

def getConnection():
    return pymysql.connect(
        host='localhost',
        db='water_di',
        user='root',
        password='',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )

def tableP4():
    connection = getConnection()
    cursor = connection.cursor()
    datatable = """SELECT di_report.Date,
    MAX(CASE WHEN di_report.Site = "Fisa 2" THEN di_report.Water END) "Fisa 2",
    MAX(CASE WHEN di_report.Site = "Fisa 4" THEN di_report.Water END) "Fisa 4",
    MAX(CASE WHEN di_report.Site = "ROBOT" THEN di_report.Water END) "ROBOT"
    FROM di_report
    GROUP BY di_report.Date
    ORDER BY di_report.Date DESC
    LIMIT 31"""
    cursor.execute(datatable)
    data = cursor.fetchall()
    for i in range(len(data)): 
        keysList = list(data[i].keys())
        for key in keysList:
            if data[i][key] is None:
                data[i][key] = 0
    print(data)
    
tableP4()