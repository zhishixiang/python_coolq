#导入各种模块
from cqhttp import CQHttp
from random import choice
import json
import urllib.request
#初始化机器人
bot = CQHttp(api_root='http://127.0.0.1:5700/',
             access_token='jmMU6xP5tnLtIkLZ',
             secret='IXLzQQCtQ9yhjJKa')
def __init__(self, api_root=None, access_token=None, secret=None):
        """
        创建 CoolQ HTTP API 对象
        ------------
        :param str | None api_root: 酷 Q HTTP API 插件的监听地址的 URL ，与 HTTP API 的配置文件设定和实际使用环境相关。如果你不需要调用 API，也可以不传入。
        :param str | None access_token: 插件配置文件中所指定的 `access_token` 。如果未设定可不传此参数。
        :param str | None secret: 插件配置文件中所指定的 `secret` 。如果未设定可不传此参数。
        """
        super().__init__(api_root="127.0.0.1:5700", access_token="jmMU6xP5tnLtIkLZ", secret="IXLzQQCtQ9yhjJKa")
#获取高德地图api中的json文件
def get_record(url):
        resp = urllib.request.urlopen(url)
        ele_json = json.loads(resp.read())
        return ele_json
#监听群消息
@bot.on_message('group')
#定义自动回复的消息
def send_group_msg(event):
    #新建变量存放输入的消息 
    msg = event['message']
    #将消息根据空格分成两片方便处理
    splitmsg = msg.split()
    #当用户输入傻逼时回复的消息
    if splitmsg[0] == "傻逼":
        #所有机器人待回复的消息，需要回复时将会随机抽取
        reply = ["滚你妈的","什么孤儿东西又来送妈了","叫你爹干什么呢小杂种","智商低于0.5的傻逼东西别和我说话"]
        #发送用户输入的消息至qq号1015256551的私聊中
        bot.send_private_msg(user_id=1015256551, message=msg, auto_escape=False)
        #随机抽取一句消息回复至qq群1077550597
        bot.send_group_msg(group_id=1077550597, message=choice(reply), auto_escape=False)
    #当用户输入的消息为天气时回复的消息
    if splitmsg[0] == "天气":
        if __name__ == '__main__':
            #读取城市编码
            f = open('list.json',encoding='utf-8')
            citycodeall = f.read()
            citycodeall = json.loads(citycodeall)
            #调换值和键的方法
            def get_key1(dct, value):
                return list(filter(lambda k:dct[k] == value, dct))
            #用值调换字典内的键，传入的键为用户查询的城市，查询语法为：天气 城市名（比如天气 广州市）
            b = get_key1(citycodeall,splitmsg[1])
            #将调换的列表转换为字符串
            citycode = str(b[0])
            #获取json
            weatherjson = get_record('https://restapi.amap.com/v3/weather/weatherInfo?city=%s&key=b5874fa2247c68210bc585cc23575bba&extensions=base'%citycode)
            #从json中获取各种消息
            province = (weatherjson["lives"][0]["province"])
            city = (weatherjson["lives"][0]["city"])
            weather = (weatherjson["lives"][0]["weather"])
            time = (weatherjson["lives"][0]["reporttime"])
            temperature = (weatherjson["lives"][0]["temperature"])
            #回复用户
            reply = ("%s省%s当前天气为%s 气温为%s度 最后更新时间为%s"%(province,city,weather,temperature,time))
            bot.send_group_msg(group_id=1077550597, message=reply, auto_escape=False)
#运行机器人
bot.run(host='127.0.0.1', port=8080, debug=True)
