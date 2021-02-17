from flask import Flask, render_template, send_from_directory, redirect, session, request, escape, jsonify
from jinja2 import Environment
from jinja2.loaders import FileSystemLoader
from flask_sqlalchemy import SQLAlchemy 
import requests
import os
from datetime import datetime
from addict import Dict
import json
app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET")
apiKey = os.environ.get("FLASK_SECRET")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
destWebhook = os.environ.get("WEBHOOK_URL")
mainSite = os.environ.get("PUBLIC_SITE")
serverHeartBeats = Dict()
db = SQLAlchemy(app)

class InfoLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    content = db.Column(db.Text)
    date = db.Column(db.DateTime)
print(apiKey)

db.create_all()
db.session.commit()

@app.route("/")
def redirMain():
    return ("<script>location.replace('"+mainSite+"')</script>")

@app.route("/v1/inbound/message", methods=['POST'])
def msgLog():
    req_data = request.get_json()
    api_Key = req_data['API_KEY']
    time = datetime.now()
    title = req_data['TITLE']
    content = req_data['CONTENT']
    print(content)
    if apiKey == api_Key:
        data = InfoLog(title=title, date=time, content=content)
        try:
            db.session.add(data)
            db.session.commit()
            return "200 OK", 200
        except:
            return "500 Internal Server Error", 500
    else:
        return "401 Unauthorized", 401
@app.route("/v1/outbound/message", methods=["POST"])
def getMsgLog():
    req_data = request.get_json()
    api_Key = req_data['API_KEY']
    logs = InfoLog.query.order_by(InfoLog.date.desc()).all()
    targdict = Dict()
    for x in logs:
        targdict['__'].setdefault(str(x.date),{})
        targdict['__'][str(x.date)].setdefault(x.title,x.content)

    resp = app.response_class(response=json.dumps(targdict),status=200,mimetype="application/json")
    return resp

@app.route("/v1/rc", methods=['POST'])
def checkRegionalCoord():
    req_data = request.get_json()
    api_Key = req_data['API_KEY']
    time = req_data['TIMESTAMP']
    service = req_data['DAEMON']
    result = req_data['STATUS']
    location = req_data['LOCATION']
    dtime = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
    content = " **Problem** detected with" + ' '+"**"+ service +"**" + ' '+ "currently reporting as" + ' ' + result[:-1] + ' ' + "at" + ' ' + time + ' ' + "at" + ' ' + location
    if apiKey == api_Key:
        data = InfoLog(title=location+" RC Systemd Logger", date=dtime, content="Daemon: "+service+" Status: "+result)
        try:
            db.session.add(data)
            db.session.commit()
            s = webhookSend(content,"Server")    
            return "200 OK", 200
        except:
            return "500 Internal Server Error", 500
    else:
        return "401 Unauthorized", 401


@app.route("/v1/node/heartbeat", methods=['POST'])
def heartBeatReceive():
    req_data = request.get_json()
    api_Key = req_data['API_KEY']
    time = req_data['TIMESTAMP']
    location = req_data['LOCATION']
    node_id = req_data['NODE_ID']
    serverHeartBeats['HBLog'].setdefault(node_id,str(time))
    

@app.route("/v1/node", methods=['POST'])
def checkNode():
    req_data = request.get_json()
    time = req_data['TIMESTAMP']
    service = req_data['DAEMON']
    result = req_data['STATUS']
    location = req_data['LOCATION']
    node_id = req_data['NODE_ID']
    content = " **Problem** detected with" + ' '+"**"+ service +"**" + ' '+ "currently reporting as" + ' ' + result[:-1] + ' ' + "at" + ' ' + time + ' ' + "at" + ' ' + location
    webhookSend(content,"Server")

def webhookSend(content, endpoint):
    if endpoint == "Server":
        r = requests.post(destWebhook, headers={'User-Agent': 'Mozilla/5.0'}, data={'content':content})
        if r.status_code == 200:
            print("webhook sent")
        else:
            return 500
    elif endpoint == "Status":
        r = requests.post(destWebhook, headers={'User-Agent': 'Mozilla/5.0'}, data={'content':content})
        if r.status_code == 200:
            print("webhook sent")
            return 200
        else:
            return 500