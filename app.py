import voiceDetection as vd
from os import system
import psycopg2
import sys
from passlib.hash import pbkdf2_sha256

def login(conn, username, password):
    cursor = conn.cursor()
    query = "SELECT * FROM account WHERE username=%s"
    data = (username)
    cursor.execute(query, [data])
    records = cursor.fetchall()
    for record in records:
        if (record[1] == username and pbkdf2_sha256.verify(password, record[2])):
            return True
        break
    print ("Check your credentials!")
    return False

def set_name(conn, username, name):
    cursor = conn.cursor()
    query = "UPDATE account SET name = %s where username = %s;"
    data = (str(name), str(username))
    try:
        cursor.execute(query, data)asdadsas
        conn.commit()
    except:
        conn.rollback()
        print ("Something went wrong!")

def get_name(conn, username):
    cursor = conn.cursor()
    query = "SELECT name FROM account WHERE username=%s"
    data = (username)
    cursor.execute(query, [data])
    records = cursor.fetchall()
    return records[0][0]

def get_phone_number(conn, username):
    cursor = conn.cursor()
    query = "SELECT phone_number FROM account WHERE username=%s"
    data = (username)
    cursor.execute(query, [data])
    records = cursor.fetchall()
    return records[0][0]

def register(conn, username, password, phone_number):
    cursor = conn.cursor()
    print (username)
    query = "INSERT INTO account (username, password, phone_number) VALUES (%s, %s, %s);"
    hash = pbkdf2_sha256.hash(password)
    data = (username, hash, phone_number)
    try:
        cursor.execute(query, data)
        conn.commit()
        print ("User registered with success!")
        return True
    except:
        conn.rollback()
        print ("Something whent wrong!")
        return False

def greetings():
    conn_string = "host=host dbname=dbname user=user password=password"
    conn = psycopg2.connect(conn_string)
    user_info = {}
    user_info = init_handle(conn)
    if (user_info):
        name = user_info['name']
        username = user_info['username']
        if name is None:
            name = vd.get_name()
            set_name(conn, username, name)
    system('say Hello, {}'.format(name))
    return name, username, conn

def init_handle(conn):
    if len(sys.argv) == 3:
        if login(conn, sys.argv[1], sys.argv[2]):
            return {"username": sys.argv[1], "name": get_name(conn, sys.argv[1])}
        else:
            sys.exit(0)
    elif len(sys.argv) == 5 and (sys.argv[1] == 'r' or sys.argv[1] == 'register'):
        if register(conn, sys.argv[2], sys.argv[3], sys.argv[4]):
            if login(conn, sys.argv[2], sys.argv[3]):
                return{"username": sys.argv[2], "name": get_name(conn, sys.argv[2])}
            else:
                sys.exit(0)
        else:
            sys.exit(0)
    else:
        print ("Unexpected arguments number!")
        sys.exit(0)

def get_requests(user_name, username, conn):
    end_sentences = ['BYE', 'CLOSE', 'EXIT', 'GOODBYE']
    weather_sentences = ['TELL ME THE WEATHER', 'WEATHER']
    joke_sentences = ['TELL ME A JOKE', 'JOKE']
    recipe_sentences = ['GIVE ME A RECIPE', 'RECIPE']
    request = vd.get_request('initial')
    print (request)
    while(request.upper() not in end_sentences):
        if request.upper() in weather_sentences:
            vd.get_weather()
        elif request.upper() in joke_sentences:
            vd.get_joke()
        elif request.upper() in recipe_sentences:
            vd.get_recipe(get_phone_number(conn, username))
        elif request.upper() == 'OPEN':
            system('open http://google.pt')
        request = vd.get_request('initial')
        print (request)
    system('say See you soon, {}!'.format(user_name))

if __name__ == '__main__':
    user_name, username, conn = greetings()
    get_requests(user_name, username, conn)
