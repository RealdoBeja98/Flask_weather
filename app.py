from flask import Flask, request, redirect, render_template, url_for
import sqlite3
import requests
import pandas as pd
from collections import defaultdict
from goto import with_goto

app = Flask(__name__)
# connect to database
conn = sqlite3.connect('weather.db', check_same_thread=False)
# create cursor
cursor = conn.cursor()

# create the table
sql = ''' CREATE TABLE IF NOT EXISTS City
          (id INTEGER PRIMARY KEY AUTOINCREMENT,
          name VARCHAR(50))'''

cursor.execute(sql)


@app.route('/')
def index_get():
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=8e1bd67959ef348deb77da6f897e2146'
    # loop all in City db to take live info
    cursor.execute("SELECT name FROM City")
    all_cities_already_in_db = cursor.fetchall()
    weather_data_for_cities = []
    print(all_cities_already_in_db)
    take_cities_from_tuple = pd.DataFrame(all_cities_already_in_db)
    list_of_cities_from_tuple = take_cities_from_tuple[0].tolist()

    for iteneration_city_in_db in list_of_cities_from_tuple:
        respond_from_web = requests.get(url.format(iteneration_city_in_db)).json()
        weather = {
        'city': iteneration_city_in_db,
        'temperature': respond_from_web['main']['temp'],
        'description': respond_from_web['weather'][0]['description'],
        'icon': respond_from_web['weather'][0]['icon'],
        }
        weather_data_for_cities.append(weather)

    return render_template('weather.html', weather_data_for_cities=weather_data_for_cities)


@app.route('/', methods= ['POST'])
def index_post():
    if request.method == 'POST':
        city_taken_from_addbutton = request.form.get('city')
        # check first if city added already exists in data base
        cursor.execute("SELECT name FROM City WHERE name=? ", (city_taken_from_addbutton,))
        city_fetched = cursor.fetchone()
        if city_fetched is None:
            sql = "INSERT INTO City (name) VALUES ('{}')".format(city_taken_from_addbutton)
            cursor.execute(sql)
            conn.commit()
        return redirect(url_for('index_get'))


if __name__ == '__main__':
    app.run(debug=True)

conn.close()