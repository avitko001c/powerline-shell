import sys
import json
import pandas
import requests
from powerline_shell.utils import BasicSegment
from bs4 import BeautifulSoup

class WeatherData(BasicSegment):
    def __init__(self, powerline, seg_conf):
	    self.ip =


    def add_to_powerline(self):

    
    def get_location(self):
        url = "https://ip-geo-location.p.rapidapi.com/ip/{}".format(ip)
        querystring = {"format":"json"}
        headers = {
            'x-rapidapi-host': "ip-geo-location.p.rapidapi.com",
            'x-rapidapi-key': "c5c3ac0071msh40cc459574444fap14cf49jsn89c57b96b885"
        }
        response = requests.get(url, headers=headers, params=querystring)
        data = json.loads(response.text)
        city = data['city']
        country = data['country']
        postcode = data['postcode']
        return city, country, postcode
    
    
    def get_zipcode(postcode=None):
        if postcode:
            zipcode = input('\nWelcome to the Weather Forcast\nPlease enter zip to search or press Enter for default[' + postcode + ']:') or postcode
            return zipcode
        else:
            try:
                zipcode = input('\nWelcome to the Weather Forcast\nPlease enter zip to search: ')
            except KeyError:
                zipcode = input("Please Enter Proper Zipcode: ")
        return zipcode
    
    
    def get_type(type='today'):
        try:
            type_weather = input("Please Enter the type of weather forcast: TODAY, HOURLY, FIVEDAY, or TENDAY \n").lower() or type
            return type_weather
        except KeyError:
            print("Please input a valid type: [Today, Hourly, Fiveday, Tenday]")
            sys.exit()
                
    
    def get_forcast(type_weather):
        l=[]
        # Logic to seach for particulat forcast type
        if (type_weather == 'tenday'):
            url = "https://weather.com/weather/tenday/l/"+str(zipcode)+':4:US'
            page=requests.get(url)
            content=page.content
            soup=BeautifulSoup(content,"html.parser")
            all=soup.find("div",{"class":"locations-title ten-day-page-title"}).find("h1").text
            table=soup.find_all("table",{"class":"twc-table"})
            for items in table:
                for i in range(len(items.find_all("tr"))-1):
                        d = {}
                        d["day"]=items.find_all("span",{"class":"date-time"})[i].text
                        d["date"]=items.find_all("span",{"class":"day-detail clearfix"})[i].text                        
                        d["desc"]=items.find_all("td",{"class":"description"})[i].text
                        d["temp"]=items.find_all("td",{"class":"temp"})[i].text
                        d["precip"]=items.find_all("td",{"class":"precip"})[i].text
                        d["wind"]=items.find_all("td",{"class":"wind"})[i].text
                        d["humidity"]=items.find_all("td",{"class":"humidity"})[i].text                
                        l.append(d)
        elif (type_weather == 'today'):
            url = "https://weather.com/weather/today/l/"+str(zipcode)+':4:US'
            page=requests.get(url)
            content=page.content
            soup=BeautifulSoup(content,"html.parser")
            all=soup.find("div",{"class":"today_nowcard-temp"}).find("span").text
            table=soup.find_all("div",{"class":"today_nowcard-sidecar component panel"})

            for items in table:
                for i in range(len(items.find_all("tr"))):
                        d = {}
                        d["name"]=items.find_all("th")[i].text
                        d["value"]=items.find_all("td")[i].text
                        l.append(d)
        elif (type_weather == 'hourly'):
            url = "https://weather.com/weather/hourbyhour/l/"+str(zipcode)+':4:US'
            page=requests.get(url)
            content=page.content
            soup=BeautifulSoup(content,"html.parser")
            all=soup.find("div",{"class":"locations-title hourly-page-title"}).find("h1").text
            table=soup.find_all("table",{"class":"twc-table"})
            for items in table:
                for i in range(len(items.find_all("tr"))-1):
                        d = {}
                        d["Time"]=items.find_all("span",{"class":"dsx-date"})[i].text
                        d["feels"]=items.find_all("td",{"class":"feels"})[i].text
                        d["desc"]=items.find_all("td",{"class":"description"})[i].text
                        d["temp"]=items.find_all("td",{"class":"temp"})[i].text
                        d["precip"]=items.find_all("td",{"class":"precip"})[i].text
                        d["wind"]=items.find_all("td",{"class":"wind"})[i].text
                        d["humidity"]=items.find_all("td",{"class":"humidity"})[i].text
                        l.append(d)
        elif (type_weather == 'fiveday'):
            url = "https://weather.com/weather/5day/l/"+str(zipcode)+':4:US'
            page=requests.get(url)
            content=page.content
            soup=BeautifulSoup(content,"html.parser")
            title=soup.find("div",{"class":"locations-title five-day-page-title"}).find("h1").text
            table=soup.find_all("table",{"class":"twc-table"})
            for items in table:
                for i in range(len(items.find_all("tr"))-1):
                        d = {}
                        d["Day"]=items.find_all("span",{"class":"date-time"})[i].text
                        d["High/Low"]=items.find_all("td",{"class":"temp"})[i].text
                        d["desc"]=items.find_all("td",{"class":"description"})[i].text
                        d["precip"]=items.find_all("td",{"class":"precip"})[i].text
                        d["wind"]=items.find_all("td",{"class":"wind"})[i].text
                        d["humidity"]=items.find_all("td",{"class":"humidity"})[i].text
                        l.append(d)
        else:
            print("Please Enter proper type: TODAY, HOURLY, FIVEDAY, TENDAY (Not Case Sensitive)")
            sys.exit()
        return l

    # Diplaying the output in tbale format           
    ip = requests.get('https://api.ipify.org').text
    city, country, postcode = get_location(ip)
    zipcode = get_zipcode(postcode=postcode)
    type = get_type()
    l = get_forcast(type)
    print(l)
    #df = pandas.DataFrame(l)
    #print(df)
