from flask import  Flask, request, redirect, render_template, url_for
import  sqlite3
import  requests

app = Flask(__name__)
#connect to database
conn = sqlite3.connect('weather.db', check_same_thread= False)
#create cursor
cursor = conn.cursor()

#create the table
sql = ''' CREATE TABLE IF NOT EXISTS City
          (id INTEGER PRIMARY KEY AUTOINCREMENT,
          name VARCHAR(50))'''

cursor.execute(sql)



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city_taken_from_addbutton = request.form.get('city')
        #check first if city added already exists in data base
        cursor.execute("SELECT name FROM USERS WHERE name=? ", (city_taken_from_addbutton))
        city_fetched = cursor.fetchone()
        if city_fetched is None:
            sql = "INSERT INTO City (name) VALUES ('{}')".format(city_taken_from_addbutton)
            cursor.execute(sql)
            conn.commit()
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&APPID=8e1bd67959ef348deb77da6f897e2146'

    #loop all in City db to take live info
    cursor.execute("SELECT name FROM City")
    all_cities_already_in_db = cursor.fetchone() #me duhen vetem emrat e qyteteve jo bashke me id
    
    weather_data_for_cities = []
    for iteneration_city_in_db in all_cities_already_in_db:
        respond_from_web = requests.get(url.format(iteneration_city_in_db)).json()
        weather={
           'city' : iteneration_city_in_db,
           'temperature' : respond_from_web['main']['temp'],
           'description' :  respond_from_web['weather'][0]['description'],
           'icon' : respond_from_web['weather'][0]['icon'],
        }
        weather_data_for_cities.append(weather)
        return render_template('weather.html', weather_data_for_cities = weather_data_for_cities)






if __name__ == '__main__':
    app.run(debug = True)