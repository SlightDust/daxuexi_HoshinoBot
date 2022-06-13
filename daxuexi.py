# 代码参考：Mas0nShi/antidaxuexi
import requests
import time
import datetime
import os
import json
from bs4 import BeautifulSoup

import hoshino
from hoshino import Service,priv
from hoshino import aiorequests

sv = Service(
    name = '青年大学习',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = False, #False隐藏
    enable_on_default = True, #是否默认启用
    )
    
    
# ============================================ #

startsStr = b"""section0"""
# endStr = [b'<script type="text/javascript" src="js/order.js"></script>',b'<!-- <script type="text/javascript" src="js/index.js"></script> -->',b'<!--']
endStr = [b'</body>']
optionCond = "ABCDEF"
condTemplate = "{num}. {check}"


async def get_current_info() -> dict:
    response = {
        "status": "",
        "title": "",
        "url": "",
        "errmsg": "",
        "start_time": "",
        "end_time": "",
        "cover_url": "",
    }
    url = "https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/common-api/course/current"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 8.1; PAR-AL00 Build/HUAWEIPAR-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044304 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/WIFI Language/zh_CN Process/tools"
    }
    res = await aiorequests.get(url=url, headers=headers)
    jStr = await res.json()
    _status = jStr['status']
    response['status'] = _status
    if _status == 200:
        _title = jStr['result']['title']  # 当前期数
        _startTime = jStr['result']['startTime']
        _endTime = jStr['result']['endTime']

        response['title'] = _title
        response['start_time'] = _startTime
        response['end_time'] = _endTime
        response['cover_url'] = jStr['result']['cover']
        response['url'] = jStr['result']['uri']
        
        current_time = get_current_time()
        if compare_time(_endTime, current_time):
            pass
        else:
            response['errmsg'] = f"{_title}已结束，下一期还未开始"
    else:
        response['errmsg'] = "返回码不是200，请检查页面可用性或ip是否被拉黑"
    return response


def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def compare_time(time1, time2) -> bool:
    # 比较time1是否晚于time2
    d1 = datetime.datetime.strptime(time1, '%Y-%m-%d %H:%M:%S')
    d2 = datetime.datetime.strptime(time2, '%Y-%m-%d %H:%M:%S')
    delta = d1 - d2
    if delta.days < 0:
        return False
    return True

async def parserHtml(url):
    url = url.replace("index", "m")
    res = await aiorequests.get(url=url)
    content = await res.content
    answerArrs = {"required": [], "optional": []}
    tmp = []
    sindex = content.find(startsStr)
    for i in endStr:
        _eindex = content.rfind(i)
        if _eindex != -1:
            eindex = _eindex
            break
    if sindex == -1 or eindex == -1:
        return ["喜报：获取答案失败。"]
    soup = BeautifulSoup(content[sindex:eindex], 'lxml', from_encoding='utf-8')
    for div in soup.find("body"):
        if div == "\n":
            continue
        answer = []
        try:
            for i in div.find_all("div"):
                check = i.get("data-a")
                if check is not None:
                    answer.append(check)
        except:pass

        if len(answer) > 4:
            answer = answer[:int(len(answer) / 2)]

        tmp.append(answer)
    field = "required"
    out = True
    for i, v in enumerate(tmp):
        if out and len(v) == 0 and i > 0 and len(tmp[i - 1]) != 0:
            field = "optional"
            out = False
            continue
        if len(v) != 0:
            answerArrs[field].append(v)
    # process
    output = ""
    if len(answerArrs["required"]) > 0:
        for i, v in enumerate(answerArrs["required"]):
            checks = ""
            for j, v2 in enumerate(v):
                if v2 == "1":
                    try:  # 乐了，这个ABCDEF搞崩了
                        checks += optionCond[j]
                    except: pass

            output += condTemplate.format(num=i + 1, check=checks)
            output += " "
    output += "\n"

    if len(answerArrs["optional"]) != 0:
        output += "课外习题：\n"
        for i, v in enumerate(answerArrs["optional"]):
            checks = ""
            for j, v2 in enumerate(v):
                if v2 == "1":
                    try:  # 乐了，这个ABCDEF搞崩了
                        checks += optionCond[j]
                    except:pass
            output += condTemplate.format(num=i + 1, check=checks)
            output += " "
    return output


@sv.on_fullmatch("青年大学习")
async def daxuexi(bot, ev):
    info = await get_current_info()
    if len(info['errmsg']) > 0:
        msg_with_img = info['errmsg']
        msg_pure_text = info['errmsg']
    else:
        url = info['url']
        imgCQ = f"[CQ:image,file={info['cover_url']}]"
        answer = await parserHtml(url)
        msg_with_img = f"{imgCQ}\n青年大学习{info['title']}\n开始时间{info['start_time']}\n结束时间{info['end_time']}\n答案：\n{answer}"
        msg_pure_text = f"青年大学习{info['title']}\n开始时间{info['start_time']}\n结束时间{info['end_time']}\n答案：\n{answer}"
    try:
        await bot.send(ev, msg_with_img)
    except:
        await bot.send(ev, msg_pure_text)

# ============================================ #


# 以下是推送功能
sv_push = Service(
    name = '青年大学习推送',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = False, #False隐藏
    enable_on_default = False, #是否默认启用
    )

latest_path = os.path.join(os.path.dirname(__file__), 'latest.json')

@sv_push.scheduled_job('cron', hour='7-23' ,minute='*/20')
async def check_daxuexi():
    info = await get_current_info()
    
    with open(latest_path,'r',encoding='utf-8') as jsonfile:
        latest = json.load(jsonfile)[0]
    if info['title'] == latest:
        return
    
    url = info['url']
    imgCQ = f"[CQ:image,file={info['cover_url']}]"
    answer = await parserHtml(url)
    msg_with_img = f"{imgCQ}\n检测到青年大学习更新！请注意及时完成！\n青年大学习{info['title']}\n开始时间{info['start_time']}\n结束时间{info['end_time']}\n答案：\n{answer}"
    msg_pure_text = f"检测到青年大学习更新！请注意及时完成！\n青年大学习{info['title']}\n开始时间{info['start_time']}\n结束时间{info['end_time']}\n答案：\n{answer}"
    bot = hoshino.get_bot()
    glist_info = await sv_push.get_enable_groups()
    for each_g in glist_info:
        gid = each_g
        try:
            await bot.send_group_msg(group_id=gid, message=msg_with_img)
        except:
            await bot.send_group_msg(group_id=gid, message=msg_pure_text)
    new_latest = [info['title']]
    with open(latest_path,'w',encoding='utf-8') as jsonfile:
        json.dump(new_latest, jsonfile, ensure_ascii=False, indent=4)
    
    