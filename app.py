import voiceDetection as vd
from os import system
import psycopg2
import base64
import sys
import requests


def greetings(name):
    system('say Hello {}'.format(name))

def login(conn, username, password):
    cursor = conn.cursor()
    query = "SELECT * FROM account WHERE username=%s"
    data = (username)
    cursor.execute(query, [data])
    records = cursor.fetchall()
    for record in records:
        if (record[1] == username and password == base64.b64decode(record[2])):
            return True
        break

    print ("Check your credentials!")
    return False 

def set_name(conn, username, name):
    cursor = conn.cursor()
    query = "UPDATE account SET name = %s where username = %s;"
    data = (str(name), str(username))
    print ("username = " +str(username))
    print ("name = "+ str(name))
    try:
        cursor.execute(query, data)
        conn.commit()
    except:
        conn.rollback()
        print ("Something went wrong!")

def get_name(conn, username):
    cursor = conn.cursor()
    query = "SELECT * FROM account WHERE username=%s"
    data = (username)
    cursor.execute(query, [data])
    records = cursor.fetchall()
    return records[0][3]

def register(conn, username, password):
    cursor = conn.cursor()
    print (username)
    query = "INSERT INTO account (username, password) VALUES (%s, %s);"
    data = (username, base64.b64encode(password))
    try:
        cursor.execute(query, data)
        conn.commit()
        print ("User registered with success!")
        return True
    except:
        conn.rollback()
        print ("Something whent wrong!")
        return False

def init_handle(conn):
    if len(sys.argv) == 3:
        if login(conn, sys.argv[1], sys.argv[2]):
            return {"username": sys.argv[1], "name": get_name(conn, sys.argv[1])}
        else:
            sys.exit(0)
    elif len(sys.argv) == 4 and (sys.argv[1] == 'r' or sys.argv[1] == 'register'):
        if register(conn, sys.argv[2], sys.argv[3]):
            if login(conn, sys.argv[2], sys.argv[3]):
                return{"username": sys.argv[2], "name": get_name(conn, sys.argv[2])} 
            else:
                sys.exit(0)
        else:
            sys.exit(0)

    else:
        print ("Unexpected arguments number!")
        sys.exit(0)


if __name__ == '__main__':
    end_sentences = ['BYE', 'CLOSE', 'EXIT', 'GOOD BYE']
    conn_string = "host=host_name dbname=db_name user=user password=password"
    conn = psycopg2.connect(conn_string)
    user_info = {}
    user_info = init_handle(conn)

    if (user_info):
        name = user_info['name']
        username = user_info['username']
        if name is None:
            name = vd.get_name() 
            set_name(conn, username, name)
            greetings(name)
        else:
            greetings(name)

    request = vd.get_request()

    while(request.upper() not in end_sentences):
        if request.upper() == 'WEATHER':
            vd.get_weather()
        elif request.upper() == 'TELL ME A JOKE':
            joke = requests.get('http://api.icndb.com/jokes/random').json()['value']['joke']
            joke = joke.replace("'","")
            print (joke)
            system('say {}'.format(joke))

        request = vd.get_request()
        print (request)

    system('say See you soon, {}!'.format(name))

