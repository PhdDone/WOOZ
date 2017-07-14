# -*-coding:utf-8-*-
from pymongo import MongoClient
import datetime
import glob
import os.path
import pymongo
import json
import sys
import itertools
import codecs
from pprint import pprint
import re
import os
from random import randint
import random

client = MongoClient('mongodb://localhost:27017/')

print os.environ.keys()
# client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)
# if 'DB_PORT_27017_TCP_ADDR' in os.environ.keys():

restdb = client['restdb']

hotelTaskdb = restdb.hotelTasks
taskdb = hotelTaskdb
restaurantdb = restdb.restaurant

# Task related
TASK_ID = "task_id"
USER_GOAL = "user_goal"
STATUS = "status"
CONTEXT_INFO = "context_info"
CONTEXT_TYPE = "type"  # train, flight, hotel
ANNOTATION = "annotation"

USER_RESPONSE = "user_response"
DIA_ACT = "dia_act"
SLOT_INFO = "slot_info"
SLOT_NAME = "slot_name"
SLOT_VALUE = "slot_value"

TIME_STAMP = "time_stamp"
VERSION = "version"
ANNOTATOR = "annotator"

TASK_SCHEMA = [STATUS, TASK_ID, USER_GOAL, ANNOTATION]

# Task status
NT = "newTask"
UT = "userTask"
WU = "waitForUserHit"

ANNOTATION_SCHEMA = [USER_RESPONSE, TIME_STAMP, VERSION, ANNOTATOR]

SLOT_INFO_SCHEMA = [SLOT_NAME, SLOT_VALUE]

final_flight_data = []
final_hotel_data = []
final_train_data = []

flight_goal = ["request_flight_num"]
train_goal = ["request_flight_num"]

def createOneAnnotation(rawAnnotation, version, annotator):
    res = {}
    res[USER_RESPONSE] = rawAnnotation
    res[VERSION] = version
    res[ANNOTATOR] = annotator
    res[TIME_STAMP] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return res

def checkTask(task):
    for key in TASK_SCHEMA:
        if key not in task.keys():
            # TODO: check task_id
            print "{} not in task: {}".format(key, task[TASK_ID])
            if key == ANNOTATION:
                task[key] = []
            else:
                task[key] = "*"
    return task

def checkAnnotation(annotation):
    for key in ANNOTATION_SCHEMA:
        if key not in annotation.keys():
            if key == SLOT_INFO:
                annotation[key] = []
            else:
                annotation[key] = "*"
    return annotation


def insertTask(task):
    task = checkTask(task)
    _id = taskdb.insert(task)
    return _id


def insertAnnotation(task, annotation):
    annotation = checkAnnotation(annotation)
    task[ANNOTATION].append(annotation)


def testInit():
    task1 = {TASK_ID: '1', USER_GOAL: {DIA_ACT: DIA_ACT_REQ_ALT, SLOT_NAME: "from"}, STATUS: 'userTask', CONTEXT_INFO: [{"from": "Beijing", "to": "Haikou"},{"from": "Beijing", "to":"Shijiazhuang"}], ANNOTATION: []}
    task2 = {TASK_ID: '2', USER_GOAL: {DIA_ACT: DIA_ACT_REQ_ALT, SLOT_NAME: "from"}, STATUS: 'userTask', CONTEXT_INFO: [{"from": "Beijing", "to": "Haikou"},{"from": "Beijing", "to":"Shijiazhuang"}], ANNOTATION: []}
    insertTask(task1)
    insertTask(task2)
    print hotelTaskdb.find_one({TASK_ID: '1'})
    print hotelTaskdb.count()

def dropHotelTaskDB():
    hotelTaskdb.drop()

def loadRestaurantData():
    dropRestaurantDB()
    FILE = "./data/beijing_rest.json"
    data = []
    with codecs.open(FILE, 'rU', 'utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    for restaurant in data:
        res = checkRestaurant(restaurant)
        restaurantdb.insert(res)

def loadHotelUserGoals():
    #FILE = "./data/hotelUserGoal.txt"
    FILE = "./data/edct2UserGoal.json"
    data = []
    with codecs.open(FILE, 'rU', 'utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    return data

def createHotelTasks():
    dropHotelTaskDB()
    taskId = 0;
    userGoals = loadHotelUserGoals()
    for userGoal in userGoals:
        newTask = {TASK_ID: str(taskId),
                   USER_GOAL: userGoal,
                   ANNOTATION: []}
        hotelTaskdb.insert(newTask)
        taskId += 1

def loadHotelData():
    basePath = "/Users/yuanzhedong/Documents/mobvoi/smp2017/data/Task2data/hotel"
    for filename in os.listdir(basePath):
        with codecs.open(basePath + "/" + filename, 'rU', 'utf-8') as f:
            for line in f:
                final_hotel_data.append(json.loads(line))
    print len(final_hotel_data)
    print final_hotel_data[0]


def loadFlightData():
    basePath = "/Users/yuanzhedong/Documents/mobvoi/smp2017/data/Task2data/flight"
    flight_data = []
    for filename in os.listdir(basePath):
        data_file = open(basePath + "/" + filename, 'r')
        for line in data_file.readlines():
            json_data = line.strip()
            data = json.loads(json_data)
            flight_data.append(data)
    for i in range(0, len(flight_data)):
        for j in range(0, len(flight_data[i])):
            final_flight_data.append(flight_data[i][j])
    print len(final_flight_data)
    #to terminal
    #print json.dumps(final_flight_data[0], ensure_ascii=False).encode('utf-8').decode('utf-8')

    #print to file
    for i in range(0, 10):
        print json.dumps(final_flight_data[i], ensure_ascii=False).encode('utf-8')

def loadTrainData():
    basePath = "/Users/yuanzhedong/Documents/mobvoi/smp2017/data/Task2data/train"
    train_data = []
    for filename in os.listdir(basePath):
        data_file = open(basePath + "/" + filename, 'r')
        for line in data_file.readlines():
            json_data = line.strip()
            data = json.loads(json_data)
            train_data.append(data)
    for i in range(0, len(train_data)):
        for j in range(0, len(train_data[i])):
            final_train_data.append(train_data[i][j])
    #print len(final_train_data)

    contexts = []
    idxs = random.sample(range(1, len(final_train_data)), 50)
    for idx in idxs:
        if idx < 1 or idx == len(final_train_data) - 1: continue
        else:
            print json.dumps(final_train_data[idx-1], ensure_ascii=False).encode('utf-8')
            print json.dumps(final_train_data[idx], ensure_ascii=False).encode('utf-8')
            print json.dumps(final_train_data[idx+1], ensure_ascii=False).encode('utf-8')

    #for i in range(0, len(final_train_data)):
        #print json.dumps(final_train_data[i], ensure_ascii=False).encode('utf-8')
    #50 context lists
    #generateTrainContext()

'''
Take slot and dialogue_act and generate goals
'''

def generate_goal():
    return None
def generate_task_json():
    '''
    load db (done)
    load goal
    print json file
    :return:
    '''
    return None


hotelSample = {u'city': u'\u897f\u5b89', u'name': u'\u4e34\u6f7c\u4e1c\u6d77\u62db\u5f85\u6240',
               u'gpsLat': 34.38636717523, u'price': u'0', u'gpsLng': 109.229480385021,
               u'address': u'\u94f6\u6865\u5927\u905356\u53f72\u697c(\u4ea4\u8b66\u5927\u961f\u5357\u90bb)'}
trainSample = {u'terminalStation': u'\u5317\u4eac\u5357', u'originStation': u'\u4e0a\u6d77',
               u'price': [{u'name': u'\u4e8c\u7b49\u5ea7', u'value': u'309'},
                          {u'name': u'\u8f6f\u5367', u'value': u'693'}], u'trainNo': u'D322',
               u'trainType': u'\u52a8\u8f66', u'startTime': u'2017-04-18 19:53', u'arrivalTime': u'2017-04-19 07:45',
               u'runTime': u'11\u5c0f\u65f652\u5206'}
flight = {u'departCity': u'\u5317\u4eac', u'standardPrice': u'1640.0000', u'flight': u'SC1437',
          u'aPort': u'\u6c5f\u5317\u56fd\u9645\u673a\u573a', u'takeOffTime': u'2017-04-18 07:00:00', u'price': u'1200',
          u'arriveCity': u'\u91cd\u5e86', u'arriveTime': u'2017-04-18 09:55:00', u'rate': u'0.73',
          u'airline': u'\u5c71\u4e1c\u822a\u7a7a\u80a1\u4efd\u6709\u9650\u516c\u53f8',
          u'dPort': u'\u9996\u90fd\u56fd\u9645\u673a\u573a', u'cabinInfo': u'\u7ecf\u6d4e\u8231', u'quantity': u'10'}

#Dialogue acts bind with slot
DIA_ACT_INFORM = "inform" #帮我找个北京的酒店
DIA_ACT_REQEST = "request" #这家酒店叫什么, 航班号是多少
DIA_ACT_IMP_FILTER = "imp_filter" #太贵了，有没有便宜的
DIA_ACT_SELECT_WITH_SLOT = "select_with_slot" #选7：00到的那一班火车吧

#Dialogue acts bind with slot and context
DIA_ACT_REQ_WITH_SELECT = "req_with_select" #第二个票价是多少，7：30那个

#General Dialogue acts bind with any slot
DIA_ACT_DONT_CARE = "dont_care"
DIA_ACT_AFFERM = "affirm"
DIA_ACT_REJECT = "reject"

#act with no slot
DIA_ACT_SELECT = "select"
DIA_ACT_REQ_ALT = "req_alt"

'''
Request_alternatives （有别的吗，。。）
Affirm/Reject (嗯，可以，不行)
Dont_care （随便，无所谓）
Selection
'''


hotelConfig = {
    "name": [DIA_ACT_INFORM, DIA_ACT_REQEST],
    "city": [DIA_ACT_INFORM],
    "address": [DIA_ACT_REQEST],
    "price": [DIA_ACT_INFORM, DIA_ACT_REQEST, DIA_ACT_IMP_FILTER],
}

def GenerateHotelUserGoal():
    goals = []
    for slotName in hotelConfig.keys():
        for diaAct in hotelConfig[slotName]:
            goal = {}
            goal[DIA_ACT] = diaAct
            goal[slotName] = slotName
            goals.append(goal)

trainConfig = {
    "terminalStation": [DIA_ACT_INFORM],
    "startTime": [DIA_ACT_INFORM],
    "originStation": [DIA_ACT_INFORM],
    "price": [DIA_ACT_INFORM],
    "arrivalTime": [DIA_ACT_INFORM],
    "trainNo": [DIA_ACT_INFORM],
    "runTime": [DIA_ACT_INFORM],
    "trainType": [DIA_ACT_INFORM],
    "seatType": [DIA_ACT_INFORM]
}

flightConfig = {
    "aPort": [DIA_ACT_INFORM],
    "standardPrice": [DIA_ACT_INFORM],
    "flight": [DIA_ACT_INFORM],
    "price": [DIA_ACT_INFORM],
    "rate": [DIA_ACT_REQEST],
    "dPort": [DIA_ACT_INFORM],
    "departCity": [DIA_ACT_INFORM],
    "takeOffTime": [DIA_ACT_INFORM],
    "arriveTime": [DIA_ACT_INFORM],
    "arriveCity": [DIA_ACT_INFORM],
    "airline": [DIA_ACT_INFORM],
    "cabinInfo": [DIA_ACT_INFORM],
    "quantity": [DIA_ACT_INFORM]
}


def generate_user_goal():
    for key in flight.keys():
        print key

def generateRandomTaskId(count):
    taskId = randint(0, count-1)
    return str(taskId)

if __name__ == "__main__":
    # init()

    #loadRestaurantData()
    # getAllFoodType()
    # getAllAreaName()
    # testSearchDB()
    # logging.basicConfig(filename='app.log',level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    # loadTask()
    # buildQueryKey()
    # resetWWtoWT()
    # resetWUtoUT()
    # chooseByColum(FOOD_TYPE)
    #loadFlightData()
    loadTrainData()
    #loadHotelData()
    # generate_user_goal()
    # generate_user_goal()
    # testInit()
    # for i in range(0, 20):
    #   print generateRandomTaskId(10)
    #generateHotelUserGoal
    #createHotelTasks()