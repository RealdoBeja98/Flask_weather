from flask import  Flask, redirect, render_template, url_for
import  sqlite3
import  requests

app = Flask(__name__)

@app.route('/')
def index():
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&APPID=8e1bd67959ef348deb77da6f897e2146'

    city = 'Las Vegas'

    respond_from_web = requests.get(url.format(city)).json()
    print(respond_from_web)

    weather={
       'city' : city,
       'temperature' : respond_from_web['main']['temp'],
       'description' :  respond_from_web['weather'][0]['description'],
       'icon' : respond_from_web['weather'][0]['icon'],
    }
    print(weather)
    return render_template('weather.html')





if __name__ == '__main__':
    app.run(debug = True)