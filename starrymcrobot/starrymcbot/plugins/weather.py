from nonebot import on_command, CommandSession
import json
import urllib.request
# on_command 装饰器将函数声明为一个命令处理器
# 这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」
@on_command('国际天气',only_to_me=False)
async def weather(session: CommandSession):
    # 从会话状态（session.state）中获取城市名称（city），如果当前不存在，则询问用户
    city = session.get('city', prompt='你想查询哪个城市的天气呢？',at_sender=True)
    # 获取城市的天气预报
    weather_report = await get_weather_of_city(city)
    # 向用户发送天气预报
    await session.send(weather_report,at_sender=True)


# weather.args_parser 装饰器将函数声明为 weather 命令的参数解析器
# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@weather.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
            # 例如用户可能发送了：天气 南京
            session.state['city'] = stripped_arg
        return

    if not stripped_arg:
        # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('要查询的城市名称不能为空呢，请重新输入')

    # 如果当前正在向用户询问更多信息（例如本例中的要查询的城市），且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg


async def get_weather_of_city(city: str) -> str:
    # 这里简单返回一个字符串
    # 实际应用中，这里应该调用返回真实数据的天气 API，并拼接成天气预报内容
    resp = urllib.request.urlopen("https://v1.alapi.cn/api/tianqi/now?city=%s"%(city))
    ele_json = json.loads(resp.read())
    country = ele_json["data"]["cnty"]
    province = ele_json['data']["admin_area"]
    realcity = ele_json["data"]["location"]
    weather = ele_json["data"]["wea"]
    degree = ele_json["data"]["tem"]
    mindegree = ele_json["data"]["tem2"]
    maxdegree = ele_json["data"]["tem1"]
    humidity = ele_json["data"]["humidity"]
    air = ele_json["data"]["air"]
    update_time = ele_json["data"]["update_time"]
    air_pm25 = ele_json["data"]["air_pm25"]
    air_level = ele_json["data"]["air_level"]
    tips = ["今日空气质量极好，无需戴口罩，适合外出","今日空气质量较差，建议有呼吸道疾病的人群不要外出","今日空气质量极差，建议戴上口罩后出行，关好门窗"]
    win = ele_json["data"]["win"]
    win_speed = ele_json["data"]["win_speed"]
    win_meter = ele_json["data"]["win_meter"]

    if air_level == "优":
        i = 0
    elif air_level == "良":
        i = 1
    elif air_level == "差":
        i = 2
    return(
        "%s %s %s 的天气情况如下:\n"
        "天气：%s\n"
        "实时气温：%s\n"
        "今日最高气温：%s\n"
        "今日最低气温：%s\n"
        "湿度：%s\n"
        "空气质量：%s\n"
        "数据更新时间：%s\n"
        "PM2.5浓度：%s\n"
        "空气质量：%s\n"
        "%s\n"
        "风向：%s\n"
        "风速：%s\n"
        "风力等级：%s\n"
        %(country,province,realcity,weather,degree,maxdegree,mindegree,humidity,air,update_time,air_pm25,air_level,tips[i],win,win_meter,win_speed)
        )
    
