import os
import json
from prettytable import PrettyTable
from pathlib import Path
from requests import get
from attrdict import AttrDict
from bs4 import BeautifulSoup
from powerline_shell.utils import ThreadedSegment
from powerline_shell import Powerline, CustomImporter

class WeatherData(ThreadedSegment):
  '''
  This is the weather segment that will reach out to weather.com and
  search a zipcode for weather data.  You can define your zipcode in
  the weather segment_conf of config.json or it will get the zipcode
  by doing a search on your external ip.  You can also define a type
  of weather data to get: hourly|today|5day|tenday: default is today
  segment_conf: weather: {
                    "type": "today"
                    "zipcode": "XXXXX"
                }
  '''

  def __init__(self, powerline, seg_conf):
    '''
    :param powerline: Powerline(args, config, theme): Defined in powerline_shell/__init__.py
    :param seg_conf: {'type': 'weather'}
    '''
    super(WeatherData, self).__init__(powerline, seg_conf)
    ip = get('https://api.ipify.org').text
    self.powerline = powerline
    self.city, self.postcode = self.get_location(ip)
    self.zipcode = self.powerline.segment_conf('weather', 'zipcode', self.postcode)
    self.type = self.powerline.segment_conf("weather", "type", "today")
    self.content = get('https://weather.com/weather/{}/l/{}:4:US'.format(self.type, self.zipcode)).content
    self.soup = BeautifulSoup(self.content, "html.parser")
    if self.type == 'today':
      self.table = self.soup.find_all("div", {"class": "today_nowcard-sidecar component panel"})
    else:
      self.table = self.soup.find_all("table", {"class": "twc-table"})

  def __call__(self):
    return self.get_data()

  @classmethod
  def get_location(cls, ip):
    url = "https://ip-geo-location.p.rapidapi.com/ip/{}".format(ip)
    querystring = {"format":"json"}
    headers = {
      'x-rapidapi-host': "ip-geo-location.p.rapidapi.com",
      'x-rapidapi-key': "c5c3ac0071msh40cc459574444fap14cf49jsn89c57b96b885"
    }
    response = get(url, headers=headers, params=querystring)
    cls.data = json.loads(response.text)
    cls.city = cls.data['city']
    cls.postcode = cls.data['postcode']
    return cls.city, cls.postcode

  def get_data(self):
    weather_data = PrettyTable()
    if self.type == 'today':
      weather_data = []
      data = AttrDict()
      data['Temp'] = self.soup.find("div", {"class": "today_nowcard-temp"}).find("span").text
      for items in self.table:
        for i in items.find_all("tr").__iter__():
          data[i.find_all("th")[0].text] = i.find_all("td")[0].text
      return data
      return weather_data
    for items in self.table:
      data = AttrDict()
      for i in items.__iter__():
        dfs = [x.text for x in items.find_all("th").__iter__()]
        days = [x.text for x in i.find_all("span", {"class": "date-time"}).__iter__()]
        data['Day'] = days
        dates = [x.text for x in i.find_all("span", {"class": "day-detail clearfix"}).__iter__()]
        data['Date'] = dates
        descs = [x.text for x in i.find_all("td", {"class": "description"}).__iter__()]
        data['Description'] = descs
        temps = [x.text for x in i.find_all("td", {"class": "temp"}).__iter__()]
        if 'Temerature' in dfs:
          data['Temperature'] = temps
        if 'High / Low' in dfs:
          data['High / Low'] = temps
        precips = [x.text for x in i.find_all('td', {'class': 'precip'}).__iter__()]
        data['Precip'] = precips
        winds = [x.text for x in i.find_all("td", {"class": "wind"}).__iter__()]
        data['Wind'] = winds
        times = [x.text for x in i.find_all("span", {"class": "dsx-date"}).__iter__()]
        data['Time'] = times
        feels = [x.text for x in i.find_all("td", {"class": "feels"}).__iter__()]
        data['Feels'] = feels
        humiditys = [x.text for x in i.find_all("td", {"class": "humidity"}).__iter__()]
        data['Humidity'] = humiditys
    for x in data.keys():
      info = data[x]
      if info:
        weather_data.add_column(x, info)
    return weather_data, data

      #for i in range(len(items.find_all("tr"))):
      #  try:
      #    if items.find_all("th")[i].text == 'Time':
      #      data[items.find_all('th')[i].text] = items.find_all("span", {"class": "dsx-date"})[i].text
      #    if items.find_all("th")[i].text == 'Temp':
      #      data[items.find_all("th")[i].text] = items.find_all("td", {"class": "temp"})[i].text
      ##    if items.find_all("th")[i].text == 'High / Low':
      #      data[items.find_all("th")[i].text] = items.find_all("td", {"class": "temp"})[i].text
      #    if items.find_all("th")[i].text == 'Feels':
      #      data[items.find_all("th")[i].text] = items.find_all("td", {"class": "feels"})[i].text
      #    if items.find_all("th")[i].text == 'Day':
      #      data[items.find_all("th")[i].text] = items.find_all("span", {"class": "date-time"})[i].text
      #    if items.find_all("th")[i].text == 'Description':
      #      data[items.find_all("th")[i].text] = items.find_all("td", {"class": "description"})[i].text
      #    if items.find_all("th")[i].text == 'Precip':
      #      data[items.find_all("th")[i].text] = items.find_all("td", {"class": "precip"})[i].text
      #    if items.find_all("th")[i].text == 'Humidity':
      #      data[items.find_all("th")[i].text] = items.find_all("td", {"class": "humidity"})[i].text
      #    if items.find_all("th")[i].text == 'Wind':
      #      data[items.find_all("th")[i].text] = items.find_all("td", {"class": "wind"})[i].text
      #  except:
      #    pass
      #  weather_data.append(data)
        #try:
          #for x in range(len(items.find_all('tr'))):
          #  data[items.find_all("th")[x].text] = items.find_all("td")[x + 1].text
          #  weather_data.append(data)
        #  print(i)
        #  for x in range(len(items.find_all('tr')[i])):
        #    data[str(items.find_all("th")[i].text) + '-{}'.format(str(i))] = items.find_all("td")[i + 1].text
        #  weather_data.append(data)
        #except:
        #  pass

        #try:
        #  data["day"] = items.find_all("span", {"class": "date-time"})[i].text
        #except (IndexError, TypeError):
        #  pass
        #try:
        #  data["date"] = items.find_all("span", {"class": "day-detail clearfix"})[i].text
        #except (IndexError, TypeError):
        #  pass
        #try:
        #  data["desc"] = items.find_all("td", {"class": "description"})[i].text
        #except (IndexError, TypeError):
        #  pass
        #try:
        #  data["temp"] = items.find_all("td", {"class": "temp"})[i].text
        #except (IndexError, TypeError):
        #  pass
        #try:
        #  data["precip"] = items.find_all("td", {"class": "precip"})[i].text
        #except (IndexError, TypeError):
        #  pass
        #try:
        #  data["wind"] = items.find_all("td", {"class": "wind"})[i].text
        #except (IndexError, TypeError):
        #  pass
        #try:
        #  data["time"] = items.find_all("span", {"class": "dsx-date"})[i].text
        #except (IndexError, TypeError):
        #  pass
        #try:
        #  data["feels"] = items.find_all("td", {"class": "feels"})[i].text
        #except (IndexError, TypeError):
        #  pass
        #try:
        #  data["humidity"] = items.find_all("td", {"class": "humidity"})[i].text
        #except (IndexError, TypeError):
        #  pass
        #if not len(data) == 0:
    #weather_data.append(data)
    #ret#un weather_data

  def parse_data(self):
    # Logic to seach for particulat forcast type
    weather_data = self.get_data()
    return weather_data

args = AttrDict()
args.loglevel = 'info'
args.shell = 'bash'
args.config = AttrDict(json.loads(Path(os.path.expanduser('~/.config/powerline-shell/config.json')).read_bytes()))
args.config['weather']['type'] = '5day'
custom_importer = CustomImporter()
theme_mod = custom_importer.import_(
        "powerline_shell.themes.",
        args.config.get("theme", "default"),
        "Theme")
theme = getattr(theme_mod, "Color")
seg_conf = {'type': 'weather'}
powerline = Powerline(args, args.config, theme)
weather = WeatherData(powerline, seg_conf)
out, data = weather.get_data()
