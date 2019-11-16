import urllib
import urllib.request
import urllib.parse
import json


APPKEY='07921982a24cc49f33a38c0fb920c402'
API_URL='http://v.juhe.cn/weather/index'

def _get_data(cityname=''):
    data = {}
    data['key'] = APPKEY
    data['cityname']=cityname
    url_values = urllib.parse.urlencode(data)
    url = API_URL + '?' + url_values
    result = urllib.request.urlopen(url)
    jsonarr= json.loads(result.read())
    return jsonarr
'''
# ['上海', '2017年12月22日', '星期五', '7℃~14℃', '东南风微风', '较冷', '建议着厚外套加毛衣等服装。年老体弱者宜着大衣、呢外套加羊毛衫。']
出错的情况返回-1，包含名字为空或者没有找到对应的城市
'''
def today(cityname=''):
    if cityname == '':
        return -1
    res = _get_data(cityname)
    if res['result'] is None:
        return -1
    res_data = []
    res_today = res['result']['today']
    res_data.append(res_today['city'])
    res_data.append(res_today['date_y'])
    res_data.append(res_today['week'])
    res_data.append(res_today['temperature'])
    res_data.append(res_today['wind'])
    res_data.append(res_today['dressing_index'])
    res_data.append(res_today['dressing_advice'])
    return res_data
'''
[['北京', '20171222', '星期五', '-6℃~11℃', '多云', '东北风3-4 级'], ['北京', '20171223', '星期六', '-3℃~7℃', '晴转多云', '西南风微风'], ['北京', '20171224', '星期日', '-7℃~5℃', '多云转晴', '西北风3-4 级'], ['北京', '20171225', '星期一', '-6℃~4℃', '晴', '西南风微风'], ['北京', '20171226', '星期二', '-6℃~3℃', '多云', '北风微风'], ['北京', '20171227', '星期三', '-7℃~5℃', '多云转晴', '西北风3-4 级'], ['北京', '20171228', '星期四', '-3℃~7℃', '晴转多云', '西南风微风']]
出错的情况返回-1，包含名字为空或者没有找到对应的城市
'''
def week(cityname=''):
    if cityname == '':
        return -1
    res = _get_data(cityname)
    if res['result'] is None:
        return -1
    res_data = []
    res_today = res['result']['today']
    res_future = res['result']['future']
    for k,v in res_future.items():
        res_data.append([res_today['city'],v['date'],v['week'],v['temperature'],v['weather'],v['wind']])
    return res_data
