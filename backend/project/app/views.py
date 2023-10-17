from .models import *
from flask_mqtt import Mqtt
from app import app
from flask import request, jsonify, Blueprint
import base64
import json
from datetime import date
from sqlalchemy import func
import random
import string
BROCKER = 'eu1.cloud.thethings.network'
USERNAME = 'agriedge-valve-application@ttn'
app.config['MQTT_BROKER_URL'] = BROCKER
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = USERNAME
app.config['MQTT_PASSWORD'] = 'NNSXS.L4CBZ2B4BCEP7CJNC4OCYPY5QOE4CVWHDANXD5Q.V6TKVRQF6QPGLIPATT4RWEMPCZWTI7IOFETKRBXEZRAJAXEX7Q7Q' 
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_TLS_ENABLED'] = False

mqtt_client = Mqtt(app)


up_topic = "v3/" + USERNAME + "/devices/" + "#"


@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        mqtt_client.subscribe(up_topic) # subscribe topic
        #    mqtt_client.subscribe(down_topic) # subscribe topic
    else:
        print('Bad connection. Code:', rc)

@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    global counter
    global first_data
    global first_time
    # print("received")
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
        )
    # print(data["topic"])
    if data["topic"].endswith("up"):
        json_data = json.loads(data['payload'])
        try :
            feedback = json_data["uplink_message"]["decoded_payload"]["feedback"]
            with app.app_context():
                van = Van.query.filter_by(device_id = feedback["dev_id"]).first()
                rec = Record(state = feedback["fb_state"], flow = feedback["flow"], quantity = feedback["quantity"], van_id = van.id)
                # print(feedback)
                model.session.add(rec)
                model.session.commit()
        except :
            pass
    elif data["topic"].endswith("join"):
        send_last_command(data["payload"])




@app.route("/post_new_state", methods = ['POST'])
def post_new_state():
    print(request.json)
    van = Van.query.filter_by(id = request.json["id"]).first()
    if van:
        with app.app_context():
            command = Command(state = request.json["state"], van_id = van.id)
            model.session.add(command)
            model.session.commit()
        message = str(int(request.json["state"]))
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        # down_topic = "v3/" + USERNAME + "/devices/" + van.device_id + "/down/push"
        down_topic = "v3/" + USERNAME + "/devices/" + van.device_id + "/down/push"
        payload = '{"downlinks": [{ "f_port": 15, "frm_payload":"'+ base64_message +'", "priority": "NORMAL" }]}'
        res = mqtt_client.publish(down_topic, payload)

    return "res"


def send_last_command(payload):
    device_id = json.loads(payload)["end_device_ids"]["device_id"]
    # print(device_id)
    with app.app_context():
        van = Van.query.filter_by(device_id = device_id).first()
        command = Command.query.filter_by(van_id = van.id).order_by(Command.id.desc()).first()
    message = str(int(command.state))
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    down_topic = "v3/" + USERNAME + "/devices/" + device_id + "/down/push"
    payload = '{"downlinks": [{ "f_port": 15, "frm_payload":"'+ base64_message +'", "priority": "NORMAL" }]}'
    res = mqtt_client.publish(down_topic, payload)


@app.route("/get_history_data", methods = ["GET"])
def get_history_data():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    resp = {}    
    if start_date and end_date:
        with app.app_context():
            records = Record.query.filter(Record.date.between(start_date, end_date)).all()
            vans = Van.query.all()
            for  van in vans:
                resp[van.device_id] = []
                for rec in records:
                    if rec.van_id == van.id:
                        resp[van.device_id].append({"date":rec.date, "state": rec.state, "flow": rec.flow, "quantity": rec.quantity})
    return jsonify(resp)

@app.route("/get_history_commands", methods = ["GET"])
def get_history_commands():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    resp = {}    
    if start_date and end_date:
        with app.app_context():
            commands = Command.query.filter(Command.date.between(start_date, end_date)).all()
            vans = Van.query.all()
            for  van in vans:
                resp[van.device_id] = []
                for command in commands:
                    if command.van_id == van.id:
                        resp[van.device_id].append({"date":command.date, "state": command.state})
    return jsonify(resp)


@app.route("/get_parcel_list", methods = ["GET"])
def get_parcel_list():
    resp = []
    with app.app_context():
        parcels = Parcel.query.all()
        for parcel in parcels:
            vans = Van.query.filter_by(parcel_id = parcel.id)
            states = {"on":0, "off":0}
            for van in vans:
                last_rec = Record.query.filter_by(van_id = van.id).order_by(Record.id.desc()).first()
                if last_rec:
                    if last_rec.state:
                        states["on"]+=1
                    else:
                        states["off"]+=1
            resp.append({
                "id":parcel.id,
                "name":parcel.name.upper(),
                "location":parcel.location,
                "surface":parcel.surface,
                "states":states
            })
    return jsonify(resp)

@app.route("/add_parcel", methods = ["POST"])
def add_parcel():
    data = request.json
    print(data)
    user = User.query.filter_by(id = 0).first()
    with app.app_context():
        parcel = Parcel(name = data["name"], location = data["location"], surface = data["surface"], user_id = user.id)
        model.session.add(parcel)
        model.session.commit()
    return jsonify("done")


@app.route("/get_van_list", methods = ["GET"])
def get_van_list():
    resp = {}
    with app.app_context():
        parcel = Parcel.query.filter_by(id = request.args["id"]).first()
        if parcel:
            resp["parcel"]={
                "id":parcel.id,
                "name" : parcel.name.upper(),
                "location" : parcel.location,
                "surface" : parcel.surface,
            }
            vans = Van.query.filter_by(parcel_id = request.args["id"])
            resp["vans"] = []
            for van in vans:
                last_rec = Record.query.filter_by(van_id = van.id).order_by(Record.id.desc()).first()
                last_com = Command.query.filter_by(van_id = van.id).order_by(Command.id.desc()).first()
                if last_rec and last_com:
                    resp["vans"].append({
                        "id":van.id,
                        "name":van.name,
                        "device_id":van.device_id,
                        "com_state":last_com.state,
                        "rec_state":last_rec.state,
                        "flow":last_rec.flow,
                        "quantity":last_rec.quantity,
                        "battery":round(last_rec.battery, 2)
                    })
                else:
                    resp["vans"].append({
                        "id":van.id,
                        "name":van.name,
                        "device_id":van.device_id,
                        "com_state":False,
                        "rec_state":False,
                        "flow":0,
                        "quantity":0,
                        "battery":0
                    })
                    
    return jsonify(resp)

@app.route("/add_van", methods = ["POST"])
def add_van():
    data = request.json
    print(data)
    user = User.query.filter_by(id = 0).first()
    with app.app_context():
        parcel = Parcel.query.filter_by(id = data["parcel_id"]).first()
        if parcel:
            van = Van(name = data["van"]["name"], device_id = data["van"]["device_id"], parcel_id = parcel.id)
            model.session.add(van)
            model.session.commit()
    return jsonify("done")


@app.route("/edit_parcel", methods = ["POST"])
def edit_parcel():
    data = request.json
    user = User.query.filter_by(id = 0).first()
    res = {}
    with app.app_context():
        parcel = Parcel.query.filter_by(id=data["parcel"]["id"]).first()
        if parcel:
            parcel.name = data["parcel"]["name"]
            parcel.location = data["parcel"]["location"]
            parcel.surface = data["parcel"]["surface"]
            model.session.commit()

    return jsonify(res)

@app.route("/delete_parcel", methods = ["POST"])
def delete_parcel():
    data = request.json
    user = User.query.filter_by(id = 0).first()
    with app.app_context():
        parcel = Parcel.query.filter_by(id=data["id"]).first()
        if parcel:
            model.session.delete(parcel)
            model.session.commit()
        print(parcel)
    return jsonify("res")




@app.route("/get_van_data", methods = ["GET"])
def get_van_data():
    id = request.args["id"]
    resp = {}
    with app.app_context():
        van = Van.query.filter_by(id = id).first()
        recs = Record.query.filter_by(van_id = van.id)
        last_rec = Record.query.filter_by(van_id = van.id).order_by(Record.id.desc()).first()
        last_com = Command.query.filter_by(van_id = van.id).order_by(Command.id.desc()).first()
        resp["van"] = {
            "id":van.id,
            "parcel_id":van.parcel_id,
            "name":van.name,
            "device_id":van.device_id,
            "rec_state":last_rec.state,
            "com_state":last_com.state
        }
        resp["flow_values"] = {
            "time":[],
            "values":[],
        }
        if recs:
            if recs.count()>20:
                recs = recs[0:19]
                print("yessss")
            for rec in recs:
                resp["flow_values"]["time"].append(
                    rec.date.strftime("%H:%M:%S")
                )
                resp["flow_values"]["values"].append(
                    rec.flow
                )
    return jsonify(resp)

@app.route("/edit_van", methods = ["POST"])
def edit_van():
    data = request.json
    user = User.query.filter_by(id = 0).first()
    res = {}
    with app.app_context():
        van = Van.query.filter_by(id=data["id"]).first()
        if van:
            van.name = data["name"]
            van.device_id = data["device_id"]
            model.session.commit()

    print(data)
    return jsonify("res")

@app.route("/delete_van", methods = ["POST"])
def delete_van():
    data = request.json
    user = User.query.filter_by(id = 0).first()
    with app.app_context():
        van = Van.query.filter_by(id=data["id"]).first()
        if van:
            model.session.delete(van)
            model.session.commit()
        print(van)
    print(data)
    return jsonify("res")

@app.route("/create_data", methods = ["GET"])
def create_data():
    # S = 10
    # with app.app_context():
    #     parcels = Parcel.query.all()
    #     for parcel in parcels:
    #         for i in range(random.randint(4, 10)):
    #             device_id = str(''.join(random.choices(string.ascii_uppercase + string.digits, k = S)))
    #             name = str(''.join(random.choices(string.ascii_uppercase + string.digits, k = S)))
    #             van = Van(name = name, device_id = device_id, parcel_id=parcel.id)
    #             model.session.add(van)
    #             model.session.commit()

    with app.app_context():
        vans = Van.query.all()
        for van in vans:
            rec = Record(state = random.randint(0,1), flow = random.randint(0,5), quantity = random.randint(0,500), battery = random.uniform(10,12),  van_id = van.id)
            model.session.add(rec)
            model.session.commit()
   
    with app.app_context():
        recs = Record.query.all()
        for rec in recs:
            com = Command(state = rec.state, van_id = rec.van_id)
            model.session.add(com)
            model.session.commit()

    return "res"

