import requests

import json

print('Welcome to Weather Application')

print('submit city name will give weather')

def get_weather_report(city=None):

    city = city
    if not city:
        city = input("City Name: ")  #taking input from user
    print("\n")
    text = "getting weather report for {} please wait".format(city) 
    print(text)

    #getting weather report from api call 
    querystring = {"id":"2172797","units":"\"metric\" or \"imperial\"","mode":"json","q":city}
    headers = {
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
        'x-rapidapi-key': "87f874e6c0mshda64261f6f315f2p188a99jsn384317c72bdd"
        }
    r = requests.get(url = "https://community-open-weather-map.p.rapidapi.com/weather", headers=headers, params=querystring)
    #if provided city name having weather report will print that
    if r.status_code == 200:
        response = r.json()
        weather_list = response['weather']
        weather = weather_list[0]
        celsius = int(response['main']['temp'])
        fahrenheit = 9.0/5.0 * celsius + 32
        print('\n')
        print("City Name:%s"%response['name'])
        print("Country:%s"%response['sys']['country'])
        print("Weather:%s"%weather['main'])
        print("Description:%s"%weather['description'])
        print("Temperature:%s"%fahrenheit)
        print("Humidity:%s"%response['main']['humidity'])
        print("Presssure:%s"%response['main']['pressure'])
        print("\n")
    else:
        print("No data available for %s"%city)
        print("Please check city name")
    user_will = input("Do you want to continue, press 'y' or 'n':")
    print("\n")
    if user_will == 'y' or user_will== 'yes':
        get_weather_report()
    else:
        print('See you again')


get_weather_report(city=None)
