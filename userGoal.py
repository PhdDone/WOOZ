#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re

import codecs
import sys
import json
import dbutil

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

SLOT_INDEX = "序号/index"

#hotel slot name
HOTEL_SLOT_PRICE = "价格/price"
HOTEL_SLOT_CITY = "城市/city"
HOTEL_SLOT_NAME = "名称/name"
HOTEL_SLOT_ADDRESS = "地址/address"

#flight_slot_name
FLIGHT_SLOT_PRICE = "价格/price"
FLIGHT_SLOT_APORT = "到达机场/aPort"
FLIGHT_SLOT_DPORT = "出发机场/dPort"
FLIGHT_SLOT_FLIGHT = "航班号/flgit"
FLIGHT_SLOT_TAKEOFFTIME = "起飞时间/takeOffTime"
FLIGHT_SLOT_ARRIVETIME = "到达时间/arriveTime"
FLIGHT_SLOT_DEPARTCITY = "出发城市/departCity"
FLIGHT_SLOT_ARRIVECITY = "到达城市/arriveCity"
FLIGHT_SLOT_CABININFO = "舱位等级/cabinInfo"
FLIGHT_SLOT_QUANTITY = "剩余票量/quantity"
FLIGHT_SLOT_STANDARDPRICE = "标准票价/stardardPrice"
FLIGHT_SLOT_PRICE = "票价/price"
FLIGHT_SLOT_RATE = "折扣/rate"

#train_slot_name
TRAIN_SLOT_TRAINNO = "车次/trainNo"
TRAIN_SLOT_TRAINTYPE = "火车类型/trainType"
TRAIN_SLOT_TERMINALSTATION = "终点站/terminalStation"
TRAIN_SLOT_ORIGINSTATION = "始发站/originStation"
TRAIN_SLOT_PRICE = "票价/price"
TRAIN_SLOT_SEATTYPE = "座位类型/seatType"
TRAIN_SLOT_STARTTIME = "开车时间/startTime"
TRAIN_SLOT_ARRIVALTIME = "到达时间/endTime"

hotelContext = [{"city": "北京", "name": "古北口怀古云舍酒店", "price": "200", "address": "北京市密云县古北口镇古下线潮河关桥南150米(原西沟风景区)"},
{"city": "北京", "name": "宽街宾馆", "price": "160", "address": "老山胡同九号"},
{"city": "北京", "name": "八渡桥头隗秀银农家院", "price": "50", "address": "十渡镇八渡桥头"},
{"city": "北京", "name": "十渡春暖小院", "price": "149", "address": "十渡镇六渡村"}
]

flightContext = [
{"departCity": "北京", "standardPrice": "1640.0000", "flight": "SC1437", "aPort": "江北国际机场", "takeOffTime": "2017-04-18 07:00:00", "price": "1200", "arriveCity": "重庆", "arriveTime": "2017-04-18 09:55:00", "rate": "0.73", "airline": "山东航空股份有限公司", "dPort": "首都国际机场", "cabinInfo": "经济舱", "quantity": "10"},
{"departCity": "北京", "standardPrice": "1640.0000", "flight": "CA1437", "aPort": "江北国际机场", "takeOffTime": "2017-04-18 07:00:00", "price": "1210", "arriveCity": "重庆", "arriveTime": "2017-04-18 09:55:00", "rate": "0.74", "airline": "中国国际航空股份有限公司", "dPort": "首都国际机场", "cabinInfo": "经济舱", "quantity": "10"},
{"departCity": "北京", "standardPrice": "1640.0000", "flight": "ZH1437", "aPort": "江北国际机场", "takeOffTime": "2017-04-18 07:00:00", "price": "1210", "arriveCity": "重庆", "arriveTime": "2017-04-18 09:55:00", "rate": "0.74", "airline": "深圳航空有限责任公司", "dPort": "首都国际机场", "cabinInfo": "经济舱", "quantity": "10"}
]

trainContext = [
    {"terminalStation": "北京南", "originStation": "上海", "price": [{"name": "二等座", "value": "309"}, {"name": "软卧", "value": "693"}], "trainNo": "D322", "trainType": "动车", "startTime": "2017-04-18 19:53", "arrivalTime": "2017-04-19 07:45", "runTime": "11小时52分"},
    {"terminalStation": "北京南", "originStation": "上海", "price": [{"name": "二等座", "value": "309"}, {"name": "软卧", "value": "693"}, {"name": "高级软卧上", "value": "1233"}, {"name": "高级软卧", "value": "1603"}], "trainNo": "D314", "trainType": "动车", "startTime": "2017-04-18 21:08", "arrivalTime": "2017-04-19 08:55", "runTime": "11小时47分"},
    {"terminalStation": "北京南", "originStation": "天津南", "price": [{"name": "二等座", "value": "54.5"}, {"name": "一等座", "value": "94.5"}, {"name": "商务座", "value": "174.5"}], "trainNo": "G164", "trainType": "高铁", "startTime": "2017-04-18 19:08", "arrivalTime": "2017-04-18 19:49", "runTime": "41分"},
    {"terminalStation": "北京", "originStation": "天津", "price": [{"name": "硬座", "value": "21.5"}, {"name": "硬卧", "value": "76.5"}, {"name": "软卧", "value": "115.5"}], "trainNo": "K1302", "trainType": "快速", "startTime": "2017-04-18 19:10", "arrivalTime": "2017-04-18 21:18", "runTime": "2小时8分"}
]


hotelTemplateSlot = {
    "inform_add_constrain" : [HOTEL_SLOT_CITY, HOTEL_SLOT_PRICE],
    "inform_remove_constrain": [HOTEL_SLOT_PRICE],
    "request": [HOTEL_SLOT_PRICE, HOTEL_SLOT_NAME, HOTEL_SLOT_ADDRESS],
    "req_with_select" : [SLOT_INDEX, HOTEL_SLOT_CITY, HOTEL_SLOT_ADDRESS, HOTEL_SLOT_NAME, HOTEL_SLOT_PRICE],
    "select_with_slot" : [SLOT_INDEX, HOTEL_SLOT_CITY, HOTEL_SLOT_ADDRESS, HOTEL_SLOT_NAME, HOTEL_SLOT_PRICE],
    "imp_filter": [],
    "yes" : [SLOT_INDEX, HOTEL_SLOT_PRICE, HOTEL_SLOT_NAME, HOTEL_SLOT_ADDRESS, HOTEL_SLOT_CITY],
    "no" : [SLOT_INDEX, HOTEL_SLOT_PRICE, HOTEL_SLOT_NAME, HOTEL_SLOT_ADDRESS, HOTEL_SLOT_CITY],
    "dont_care" : [HOTEL_SLOT_PRICE]
}

flightTemplateSlot = {
    "inform_add_constrain" : [FLIGHT_SLOT_APORT, FLIGHT_SLOT_FLIGHT, FLIGHT_SLOT_PRICE, FLIGHT_SLOT_DPORT, FLIGHT_SLOT_DEPARTCITY, FLIGHT_SLOT_TAKEOFFTIME, \
                              FLIGHT_SLOT_ARRIVETIME, FLIGHT_SLOT_ARRIVECITY, FLIGHT_SLOT_FLIGHT, FLIGHT_SLOT_CABININFO],
    "inform_remove_constrain": [FLIGHT_SLOT_APORT, FLIGHT_SLOT_FLIGHT, FLIGHT_SLOT_PRICE, FLIGHT_SLOT_DPORT, FLIGHT_SLOT_TAKEOFFTIME, \
                                FLIGHT_SLOT_ARRIVETIME, FLIGHT_SLOT_FLIGHT, FLIGHT_SLOT_CABININFO],
    "request": [FLIGHT_SLOT_APORT, FLIGHT_SLOT_FLIGHT, FLIGHT_SLOT_PRICE, FLIGHT_SLOT_DPORT, FLIGHT_SLOT_ARRIVETIME, FLIGHT_SLOT_ARRIVECITY, FLIGHT_SLOT_FLIGHT, \
                FLIGHT_SLOT_QUANTITY],
    "req_with_select" : [SLOT_INDEX, HOTEL_SLOT_CITY, HOTEL_SLOT_ADDRESS, HOTEL_SLOT_NAME, HOTEL_SLOT_PRICE],
    "select_with_slot" : [SLOT_INDEX, HOTEL_SLOT_CITY, HOTEL_SLOT_ADDRESS, HOTEL_SLOT_NAME, HOTEL_SLOT_PRICE],
    "imp_filter": [],
    "yes": [FLIGHT_SLOT_APORT, FLIGHT_SLOT_FLIGHT, FLIGHT_SLOT_PRICE, FLIGHT_SLOT_DPORT, FLIGHT_SLOT_DEPARTCITY, FLIGHT_SLOT_TAKEOFFTIME, \
            FLIGHT_SLOT_ARRIVETIME, FLIGHT_SLOT_ARRIVECITY, FLIGHT_SLOT_FLIGHT, FLIGHT_SLOT_CABININFO],
    "no": [FLIGHT_SLOT_APORT, FLIGHT_SLOT_FLIGHT, FLIGHT_SLOT_PRICE, FLIGHT_SLOT_DPORT, FLIGHT_SLOT_DEPARTCITY, FLIGHT_SLOT_TAKEOFFTIME, \
           FLIGHT_SLOT_ARRIVETIME, FLIGHT_SLOT_ARRIVECITY, FLIGHT_SLOT_FLIGHT, FLIGHT_SLOT_CABININFO],
    "dont_care": [FLIGHT_SLOT_ARRIVETIME, FLIGHT_SLOT_PRICE, FLIGHT_SLOT_FLIGHT, FLIGHT_SLOT_TAKEOFFTIME]
}

trainTemplateSlot = {
    "inform_add_constrain" : [TRAIN_SLOT_TERMINALSTATION, TRAIN_SLOT_ORIGINSTATION, TRAIN_SLOT_PRICE, TRAIN_SLOT_SEATTYPE, TRAIN_SLOT_TRAINNO, TRAIN_SLOT_TRAINTYPE, \
                              TRAIN_SLOT_STARTTIME, TRAIN_SLOT_ARRIVALTIME],
    "inform_remove_constrain": [TRAIN_SLOT_PRICE, TRAIN_SLOT_SEATTYPE, TRAIN_SLOT_TRAINNO, TRAIN_SLOT_TRAINTYPE, \
                                TRAIN_SLOT_STARTTIME, TRAIN_SLOT_ARRIVALTIME],
    "request": [TRAIN_SLOT_PRICE, TRAIN_SLOT_SEATTYPE, TRAIN_SLOT_TRAINNO, TRAIN_SLOT_TRAINTYPE, TRAIN_SLOT_STARTTIME, TRAIN_SLOT_ARRIVALTIME],
    "req_with_select" :[SLOT_INDEX, TRAIN_SLOT_SEATTYPE, TRAIN_SLOT_TRAINTYPE, TRAIN_SLOT_PRICE, TRAIN_SLOT_STARTTIME, TRAIN_SLOT_ARRIVALTIME, TRAIN_SLOT_TRAINNO],
    "select_with_slot" : [SLOT_INDEX, TRAIN_SLOT_SEATTYPE, TRAIN_SLOT_TRAINTYPE, TRAIN_SLOT_PRICE, TRAIN_SLOT_STARTTIME, TRAIN_SLOT_ARRIVALTIME, TRAIN_SLOT_TRAINNO],
    "imp_filter": [],
    "yes": [TRAIN_SLOT_ORIGINSTATION, TRAIN_SLOT_TERMINALSTATION, TRAIN_SLOT_PRICE, TRAIN_SLOT_SEATTYPE, TRAIN_SLOT_TRAINNO, TRAIN_SLOT_TRAINTYPE,TRAIN_SLOT_STARTTIME, TRAIN_SLOT_ARRIVALTIME],
    "no": [TRAIN_SLOT_ORIGINSTATION, TRAIN_SLOT_TERMINALSTATION, TRAIN_SLOT_PRICE, TRAIN_SLOT_SEATTYPE, TRAIN_SLOT_TRAINNO, TRAIN_SLOT_TRAINTYPE,TRAIN_SLOT_STARTTIME, TRAIN_SLOT_ARRIVALTIME],
    "dont_care": [TRAIN_SLOT_SEATTYPE, TRAIN_SLOT_TRAINTYPE]
}

userGoalTemplate = {
    "inform_add_constrain": "您已经告知了系统您对{domain}的部分属性的需求，现在您想告知系统关于您对{domain}的{slot}的需求",
    "inform_remove_constrain": "系统没有找到符合您偏好的结果，于是您想删除对的{slot}的偏好",
    "request": "系统为您找到了一个{domain}, 您需要询问该{domain}的{slot}",
    "imp_filter": "系统为您推荐了一些{domain}，但是您觉得系统给您推荐的结果太{早/晚/贵/便宜}了，您想要{晚/早/便宜/贵}点的",
    "req_with_select": "您需要在系统列举的多个{domain}中通过{slot_0}询问其中一个{domain}的{slot_1}",
    "select_with_slot": "系统为您找到了多个{domain}, 您需要在系统列举的多个{domain}中通过{slot}选择其中一个{domain}",
    "yes": "系统向您确认{slot}的取值，您需要肯定系统指定{domain}的{slot}",
    "no": "系统向您确认{slot}的取值，您需要否定{domain}的{slot}",
    "dont_care": "系统向您询问或确认对{domain}的{slot}的选择，您要表达对该{slot}的取值无所谓"
}

def fillTemplate(dia_act, template, domain, slots, contextInfo):
    res = []
    template2 = re.sub(r"domain", domain, template)
    #single slot
    if "{slot}" in template2:
        for slot in slots:
            user_goal_raw = re.sub(r"slot", slot, template2)
            user_goal = {"domain" : domain,
                         "dia_act" : dia_act,
                         "user_goal_raw": user_goal_raw,
                         "slot": slot
                         }
            if "select" in dia_act:
                user_goal[dbutil.CONTEXT_INFO] = contextInfo
            res.append(user_goal)
    else:
        for slot_0 in slots:
            for slot_1 in slots:
                if slot_0 != slot_1:
                    tmp = re.sub(r"slot_0", slot_0, template2)
                    user_goal_raw= re.sub(r"slot_1", slot_1, tmp)
                    user_goal = {dbutil.DIA_ACT : dia_act,
                                 "domain": domain,
                                 "user_goal_raw": user_goal_raw,
                                 "slot_0": slot_0,
                                 "slot_1": slot_1}
                    if "select" in dia_act:
                        user_goal[dbutil.CONTEXT_INFO] = contextInfo
                    res.append(user_goal)
    return res

def generateHotelUserGoal():
    for dia_act in hotelTemplateSlot.keys():
        template = userGoalTemplate[dia_act]
        userGoalDic = fillTemplate(dia_act, template, "宾馆/hotel", hotelTemplateSlot[dia_act], hotelContext)
        for userGoal in userGoalDic:
            '''line = ""
            for key in userGoal:
                line = line + "\t" + userGoal[key].decode('utf-8')
            print line
            '''
            print json.dumps(userGoal, ensure_ascii=False).decode('utf-8')

def generateFlightUserGoal():
    for dia_act in flightTemplateSlot.keys():
        template = userGoalTemplate[dia_act]
        userGoalDic = fillTemplate(dia_act, template, "航班/flight", flightTemplateSlot[dia_act], flightContext)
        for userGoal in userGoalDic:
            '''line = ""
            for key in userGoal:
                line = line + "\t" + userGoal[key].decode('utf-8')
            print line
            '''
            print json.dumps(userGoal, ensure_ascii=False).decode('utf-8')


def generateTrainUserGoal():
    for dia_act in flightTemplateSlot.keys():
        template = userGoalTemplate[dia_act]
        userGoalDic = fillTemplate(dia_act, template, "火车/train", trainTemplateSlot[dia_act], trainContext)
        for userGoal in userGoalDic:
            '''line = ""
            for key in userGoal:
                line = line + "\t" + userGoal[key].decode('utf-8')
            print line
            '''
            print json.dumps(userGoal, ensure_ascii=False).decode('utf-8')
if __name__ == "__main__":
    generateHotelUserGoal()
    generateFlightUserGoal()
    generateTrainUserGoal()