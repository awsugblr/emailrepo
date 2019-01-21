import mysql.connector
import json

dbconparamsjson = None

def get_db_con_params():
    global dbconparamsjson
    jsondata = open("./common/DBConParams.json").read()
    dbconparamsjson = json.loads(jsondata)

def invalidcontacts():
    connection, cursor = None, None
    try:
        contacts = []
        connection = mysql.connector.connect(host=dbconparamsjson["host"], user=dbconparamsjson["username"],
                                             password=dbconparamsjson["password"], database=dbconparamsjson["db"])
        # Get all invalid contacts
        sql = "SELECT * FROM Contacts WHERE DNDEmailBounce=1"
        cursor = connection.cursor()
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            contacts.append(dict(zip(columns, row)))
        if len(contacts) > 0:
            return {"result": contacts}
        else:
            return {"result": None}
    except mysql.connector.Error as err:
        return {"result": err}
    finally:
        if connection:
            connection.close()
        if cursor:
            cursor.close()


def lambda_handler(event, context):
    get_db_con_params()
    return invalidcontacts()
