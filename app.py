#-*-coding:utf-8-*-
import os
from flask import Flask,render_template, request,json
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from pymongo import MongoClient
import dbutil
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import logging
import random
import datetime
from random import randint

from logging.handlers import RotatingFileHandler

from flask import render_template, request, redirect, url_for
from flask import jsonify

app = Flask(__name__)

#app.config['MONGO_DBNAME'] = 'restdb'
#app.config['MONGO_URI'] = 'mongodb://localhost:27017/restdb'

#mongo = PyMongo(app)

admins = {
    "puyangxu@mobvoi.com": "nopassword",
    "qihu@mobvoi.com": "meiyoumima",
    "yzhdong@mobvoi.com": "mobvoi"
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/setcookie', methods = ['POST', 'GET'])
def setcookie():
    if request.method == 'POST':
        user = request.form['username']
        if 'password' in request.form.keys():
            password = request.form['password']
            resp = redirect(url_for("editTask"))
            resp.set_cookie('Password', password)
            resp.set_cookie('UserName', user)
        else:
            resp = redirect(url_for("newRandomTask"))
            resp.set_cookie('UserName', user)
        return resp

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # You should really validate that these fields
        # are provided, rather than displaying an ugly
        # error message, but for the sake of a simple
        # example we'll just assume they are provided

        user_name = request.form["name"]
        #password = request.form["password"]
        #user = db.find_by_name_and_password(user_name, password)

        #if not user:
            # Again, throwing an error is not a user-friendly
            # way of handling this, but this is just an example
        #    raise ValueError("Invalid username or password supplied")

        # Note we don't *return* the response immediately
        response = redirect(url_for("newRandomTask"))
        response.set_cookie('UserName', user_name)
        return response
    else:
        return render_template("index.html")

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        user_name = request.form["name"]
        password = request.form["password"]
        response = redirect(url_for("editTask"))
        response.set_cookie('UserName', user_name)
        response.set_cookie("Password", password)
        return response
    else:
        return render_template("admin.html")


@app.route('/')
def hello():
    return render_template('home.html')

def buildSents(sysUtc, userUtc):
    sents = []
    idx = 0
    while idx < len(sysUtc) and idx < len(userUtc):
        sents.append(sysUtc[idx])
        sents.append(userUtc[idx])
        idx += 1
    while idx < len(sysUtc):
        sents.append(sysUtc[idx])
        idx += 1
    return sents

@app.route('/task/<taskID>')
def getTaskById(taskID):
    task = dbutil.taskdb.find_one({dbutil.TASK_ID: taskID}, {'_id': False})
    if task != None:
        return json.dumps(task)
    return json.dumps({"status": "Not found"})

def checkAdmin(request):
    user_name = request.cookies.get('UserName')
    password = request.cookies.get('Password')
    if user_name in admins.keys() and admins[user_name] == password:
        return True
    return False

@app.route('/editTask', methods = ['GET'])
def editTask():
    if not checkAdmin(request):
        return redirect(url_for('admin'))

    if request.method == "GET":
        content = request.get_json()
        if content == None:
            return render_template("editTask.html")
        taskID = content[dbutil.TASK_ID]
        console.log(taskID)
        task = dbutil.taskdb.find_one({dbutil.TASK_ID: taskID}, {'_id': False})
        if task != None:
            return json.dumps(task)
        return json.dumps({"status": "Not found"})

@app.route('/searchEditTask', methods = ['POST'])
def searchEditTask():
    if not checkAdmin(request):
        return redirect(url_for('admin'))
    content = request.get_json()
    taskID = content[dbutil.TASK_ID]
    task = dbutil.taskdb.find_one({dbutil.TASK_ID: taskID}, {'_id': False})
    if task != None:
        return json.dumps(task)
    return json.dumps({"status": "Not found"})

@app.route('/submitEditTask', methods = ['POST'])
def submitEditTask():
    if not checkAdmin(request):
        return redirect(url_for('admin'))
    content = request.get_json()
    taskJson = content['task_json']
    if taskJson == None:
        return json.dumps(content)
    taskID = taskJson[dbutil.TASK_ID]
    task = dbutil.taskdb.find_one({dbutil.TASK_ID: taskID}, {'_id': False})
    if task != None:
        dbutil.taskdb.remove({dbutil.TASK_ID: taskID})
        dbutil.taskdb.insert(taskJson)
        return json.dumps(dbutil.taskdb.find_one({dbutil.TASK_ID: taskID}, {'_id': False}))
    return json.dumps({"status": "Not found"})

@app.route('/showAll')
def show_all():
    return json.dumps(list(dbutil.taskdb.find({},{'_id': False})))

@app.route('/userUpdateTask', methods=['POST'])
def userUpdateTask():
    user_name = request.cookies.get('UserName')
    if not user_name:
        return redirect(url_for('login'))
    if request.method == "POST":
        #print request
        content = request.get_json()
        taskId = content[dbutil.TASK_ID]
        rawAnnotation = content['annotation']
        rawContext = content['context']
        print rawContext
        version = 0
        if "version" in content.keys():
            version = content['version']
        annotation = dbutil.createOneAnnotation(rawAnnotation, version, user_name, rawContext)
        task = dbutil.taskdb.find_one({dbutil.TASK_ID: taskId})
        task[dbutil.ANNOTATION].append(annotation)
        dbutil.taskdb.remove({dbutil.TASK_ID: taskId})
        dbutil.taskdb.insert(task)
        app.logger.info("User %s finish a user HIT, task: %s", user_name, taskId)
        return json.dumps({'status':'OK','task_id': taskId, 'user_response': rawAnnotation})

def buildContextInfoString(contextInfo):
    res = []
    for i in range(0, len(contextInfo)):
        res.append(str(i+1) + ": " + json.dumps(contextInfo[i], ensure_ascii=False).decode('utf-8'))
    return res

def buildUserGoalString(userGoal):
    return userGoal["user_goal_raw"]

def getRandomContext(domain):
    if "hotel" in domain:
        return hotelContext[dbutil.generateRandomInt(len(hotelContext))]
    if "flight" in domain:
        return flightContext[dbutil.generateRandomInt(len(flightContext))]
    if "train" in domain:
        return trainContext[dbutil.generateRandomInt(len(trainContext))]
@app.route('/newRandomTask')
def newRandomTask():
    user_name = request.cookies.get('UserName')

    if not user_name:
        return redirect(url_for('login'))

    taskId = dbutil.generateRandomTaskId(dbutil.taskdb.count())
    print taskId
    task = dbutil.taskdb.find_one({dbutil.TASK_ID : taskId})
    if task is None:
        return render_template('noTask.html')

    taskId = task[dbutil.TASK_ID]
    contextInfo = []
    if dbutil.CONTEXT_INFO in task[dbutil.USER_GOAL].keys():
        print task
        #contextInfo = task[dbutil.USER_GOAL][dbutil.CONTEXT_INFO]
        contextInfo = getRandomContext(task[dbutil.USER_GOAL]["domain"])
    userGoal = task[dbutil.USER_GOAL]
    contextInfoStrings = buildContextInfoString(contextInfo)
    userGoalString = buildUserGoalString(userGoal)
    print userGoalString
    app.logger.info("User %s is assigned with new HIT", user_name)
    displayContext = ""
    if len(contextInfoStrings) > 0:
        displayContext = "visibility: hidden"
    return render_template('task.html', taskId=taskId, contextInfoStrings = contextInfoStrings, userGoalString = userGoalString, displayContext = displayContext)

hotelContext = []
flightContext = []
trainContext = []

if __name__=="__main__":
    logging.basicConfig(filename='app.log',level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    handler = RotatingFileHandler('foo.log', maxBytes=1000000000, backupCount=10)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    dbutil.createHotelTasks()
    hotelContext = dbutil.loadContextInfo("./data/hotel_context.json")
    flightContext = dbutil.loadContextInfo("./data/flight_context.json")
    trainContext = dbutil.loadContextInfo("./data/train_context.json")
    #dbutil.loadRestaurantData()
    app.run(host='0.0.0.0', port=9009, debug=True)
