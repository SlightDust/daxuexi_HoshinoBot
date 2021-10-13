# 代码参考：Mas0nShi/antidaxuexi



import requests
import time
import datetime

from bs4 import BeautifulSoup

import hoshino
from hoshino import Service,priv

sv = Service(
    name = '青年大学习',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = False, #False隐藏
    enable_on_default = True, #是否默认启用
    )
    
    
# ============================================ #

startsStr = b""" <div class="section0 topindex">"""
endStr = b'<script type="text/javascript" src="js/order.js"></script>'
optionCond = "ABCDEF"
condTemplate = "{num}. {check}"


def get_current_info() -> dict:
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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
    }
    res = requests.get(url=url, headers=headers)
    jStr = res.json()
    # print(jStr)
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

        current_time = get_current_time()
        if compare_time(_endTime, current_time):
            response['url'] = jStr['result']['uri']
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


def testFunc():
    data = requests.get("https://h5.cyol.com/special/weixin/sign.json").json()
    for d in data:
        print(data[d]["url"])
        # print(parserHtml(data[d]["url"]))


def parserHtml(url):
    content = requests.get(url=url).content
    answerArrs = {"required": [], "optional": []}
    tmp = []
    # print(content.decode())
    sindex = content.find(startsStr)
    eindex = content.rfind(endStr)
    if sindex == -1 or eindex == -1:
        return []
    soup = BeautifulSoup(content[sindex:eindex], 'lxml', from_encoding='utf-8')
    for div in soup.find("body"):
        if div == "\n":
            continue
        answer = []
        for i in div.find_all("div"):
            check = i.get("data-a")
            if check is not None:
                answer.append(check)

        if len(answer) > 4:
            answer = answer[:int(len(answer) / 2)]

        tmp.append(answer)
        # print("--------------------------------------------------------")
    # print(tmp)
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
                    checks += optionCond[j]

            output += condTemplate.format(num=i + 1, check=checks)
            output += " "
    output += "\n"

    if len(answerArrs["optional"]) != 0:
        output += "课外习题：\n"
        for i, v in enumerate(answerArrs["optional"]):
            checks = ""
            for j, v2 in enumerate(v):
                if v2 == "1":
                    checks += optionCond[j]
            output += condTemplate.format(num=i + 1, check=checks)
            output += " "
    # print(answerArrs)
    return output


@sv.on_fullmatch("青年大学习")
async def daxuexi(bot, ev):
    info = get_current_info()
    if len(info['errmsg']) > 0:
        msg = info['errmsg']
    else:
        url = info['url']
        imgCQ = f"[CQ:image,file={info['cover_url']}]"
        answer = parserHtml(url)
        msg_with_img = f"{imgCQ}\n青年大学习{info['title']}\n开始时间{info['start_time']}\n结束时间{info['end_time']}\n答案：\n{answer}"
        msg_pure_text = f"青年大学习{info['title']}\n开始时间{info['start_time']}\n结束时间{info['end_time']}\n答案：\n{answer}"
        
    #print(msg)
    # await bot.send(ev, imgCQ)
    try:
        await bot.send(ev, msg_with_img)
    except aiocqhttp.exceptions.ActionFailed:
        await bot.send(ev, msg_pure_text)
    # get_current_time()
    # testFunc()