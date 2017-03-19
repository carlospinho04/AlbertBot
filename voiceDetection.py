import speech_recognition as sr
from os import system
import requests
import send_messages as sm
import random

m = sr.Microphone()
r = sr.Recognizer()

def get_audio():
    with sr.Microphone() as source:
        print('Say something!')
        audio = r.listen(source)
    return (audio)

def get_min_threshold():
    with m as source: r.adjust_for_ambient_noise(source)

def get_request(state):
    try:
        system('say What do you want?') if state == 'initial' else system('say Wich recipe do you want?')
        get_min_threshold()
        request =  r.recognize_google(get_audio())
    except:
        request = None

    while (request is None):
        system('say Sorry, can not understand you.')
        try:
            get_min_threshold()
            system('say What do you want?') if state == 'initial' else system('say Which recipe do you want?')
            request =  r.recognize_google(get_audio())
        except:
            request = None
    return request

def get_name():
    answer = 'no'
    while (answer == 'no'):
        get_min_threshold()
        system('say What is your name?')
        try:
            name =  r.recognize_google(get_audio())
            system('say Your name is {} ?'.format(name))
            try:
                answer = r.recognize_google(get_audio())
            except:
                system('say Cannot find the information that you want')
        except:
            system('say Cannot find the information that you want')
    return (name)

def get_recipe(phone_number):
    recipe = get_request('recipe')
    try:
        food = requests.get('https://api.edamam.com/search?q={}&app_id=appid&app_key=appkey'.format(recipe)).json()
        ingredients = ''
        selected_recipe = random.choice(food['hits'])
        for ingredient in selected_recipe['recipe']['ingredientLines']:
            ingredients += ingredient + '\n'
        ingredients += "Site: \n"
        ingredients += food['hits'][1]['recipe']['url']
        sm.send_message(phone_number, ingredients)
    except:
        system('say Sorry, something went wrong!')

def get_joke():
    joke = requests.get('http://api.icndb.com/jokes/random').json()['value']['joke']
    joke = joke.replace("'","")
    print (joke)
    system('say {}'.format(joke))

def get_weather():
    get_min_threshold()
    system('say Which city do you want to know the weather for?')
    try:
        city = r.recognize_google(get_audio())
        weather = requests.get('http://api.openweathermap.org/data/2.5/weather?q={}&appid=appid'.format(city)).json()
        temperature = float("{0:.1f}".format(weather['main']['temp'] - 273.15))
        system('say The current weather for {} is {} and the temperature is {} degrees'.format(weather['name'], weather['weather'][0]['main'], temperature))
    except:
        system('say Cannot find the information that you want')
