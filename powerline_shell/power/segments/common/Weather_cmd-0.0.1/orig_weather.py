import requests
from bs4 import BeautifulSoup
import pandas


top_cities = ['Mumbai','Delhi','Banglore','Chennai','Kolkata','Ahmedabad','Hyderabad','Pune','Surat','Jaipur','Lucknow','Chandigarh']

# Mentioning secure url for particular cities(couldn't get the post request parameteres here)
cities =  {

        'Mumbai'  :  '03343c09f067e51a168a3b28e5a26f73d9592bf6e527ea139c4651e7c33d5429',
        'Delhi'   :  'aff9460b9160c73ff01769fd83ae82cf37cb27fb7eb73c70b91257d413147b69',
        'Banglore':  '072e7110ccda5a2b786e1b942f4946d382bdd6ff315f63682bfc14827786c271',
        'Chennai' :  'db1e2342716e8c57c40b728ac1c43ce012289a41d1c10de9a76ba1777a8de974',
        'Kolkata' :  '93129bd249f38a036dca3f85c159235f0e109334e73454e7d1251d904979ad69',
        'Ahmedabad': '32d9f01e7c7d1aa747578e8e259740ed90a201c5e8296409c7c4027de23b0bef',
        'Hyderabad' : 'aae85713f4116f0df6272434cd21b951eb301a98b5444ea28a1999cc6956c88b',
        'Pune'    :  'be492ef2b9cd0f22546647484a4b32c3a782242720977da71d6c1476c1c64ca1',
        'Surat'   :  'b5bad2446dccf71edee766ca180e85d656510dd00c2c1e675fd9792279c3d2c2',
        'Jaipur'  :  '4eaebb7e8b45bf3cd0757e13388de718f80a0835043d432373f96f3c835be530',
        'Lucknow' :  '5ec225a756fce4fad752b767b5d69df3263c43b343fe70922de7534a92dabe52',
        'Chandigarh':'6355edc75bc487c9b494eafd070afd21a6e6e5452c54761b84b6718830a09d20'
}

# Taking input for city name and type of forcast
try:
    print('-------------Welcome to the Weathe Forcast------------------')
    print("Please Select top citied from here (Case sensitive) : ")
    print(',  '.join(map(str,top_cities)))
    city = input()
    url = "https://weather.com/en-IN/weather/"+str(cities[city])
   

except KeyError:
    print("Please Enter Proper City name from below (Case sensitive)")
    print(',  '.join(map(str,top_cities)))


if city in top_cities:
     type_weather = input("Please Enter the type of weather forcast: 0 for TODAY : 1 for HOURLY:  2 for 5DAYS : 3 for 10DAYS \n")
     print("-------Searching-------------------")
    

else:
    city = input()
    url = "https://weather.com/en-IN/weather/"+str(cities[city])
    type_weather = input("Please Enter the type of weather forcast: 0 for TODAY : 1 for HOURLY:  2 for 5DAYS : 3 for 10DAYS \n")
    print("-------Searching-------------------")
    


l=[]
# Logic to seach for particulat forcast type
if (type_weather == '3'):
    url = "https://weather.com/en-IN/weather/tenday/l/"+str(cities[city])
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
   

elif (type_weather == '0'):
    url = "https://weather.com/en-IN/weather/today/l/"+str(cities[city])
    page=requests.get(url)
    content=page.content
    soup=BeautifulSoup(content,"html.parser")
    all=soup.find("div",{"class":"today_nowcard-temp"}).find("span").text
    print('temperature:',all)
    table=soup.find_all("div",{"class":"today_nowcard-sidecar component panel"})

    for items in table:
	    for i in range(len(items.find_all("tr"))):
		    d = {}
		    d["name"]=items.find_all("th")[i].text
		    d["value"]=items.find_all("td")[i].text			
		    l.append(d)
elif (type_weather == '1'):
    url = "https://weather.com/en-IN/weather/hourbyhour/l/"+str(cities[city])
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
		    d["desc"]=items.find_all("td",{"class":"hidden-cell-sm description"})[i].text
		    d["temp"]=items.find_all("td",{"class":"temp"})[i].text
		    d["precip"]=items.find_all("td",{"class":"precip"})[i].text
		    d["wind"]=items.find_all("td",{"class":"wind"})[i].text
		    d["humidity"]=items.find_all("td",{"class":"humidity"})[i].text		
		    l.append(d)

elif (type_weather == '2'):
    url = "https://weather.com/en-IN/weather/5day/l/"+str(cities[city])
    page=requests.get(url)
    content=page.content
    soup=BeautifulSoup(content,"html.parser")
    all=soup.find("div",{"class":"locations-title five-day-page-title"}).find("h1").text
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
    print("Please Enter Proper input")   

# Diplaying the output in tbale format           
df = pandas.DataFrame(l)
print(df)
df.to_csv("output.csv")	
