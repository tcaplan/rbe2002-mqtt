from tkinter import *
from paho.mqtt import client as mqtt_client
import json
import os
from dotenv import load_dotenv

load_dotenv()

broker = os.getenv('MQTT_SERVER')
port = int(os.getenv('MQTT_PORT'))
topic = "team5"
topic_sub = "team5/sensors/#"
# generate client ID with pub prefix randomly
username = os.getenv('MQTT_USER')
password = os.getenv('MQTT_PASS')

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc==0:
            print("Successfully connected to MQTT broker")
        else:
            print("Failed to connect, return code %d", rc)


    client = mqtt_client.Client(protocol=mqtt_client.MQTTv311)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client,status):
    # msg = f"messages: {msg_count}"
    msg = "{\"action\":\"command/insert\",\"command\":{\"command\":\"LED_control\",\"parameters\":{\"led\":\""+status+"\"}}}"
    # msg = '{"action":"command/insert","command":{"id":432436060,"command":"LED_control","timestamp":"2021-03-24T00:19:44.418","lastUpdated":"2021-03-24T00:19:44.418","userId":37,"deviceId":"s3s9TFhT9WbDsA0CxlWeAKuZykjcmO6PoxK6","networkId":37,"deviceTypeId":5,"parameters":{"led":"on"},"lifetime":null,"status":null,"result":null},"subscriptionId":1616544981034531}'
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):

        # looking for the topic team5/dashboard/ID where ID is the ID number of the romi
        # then looks for 4 numbers spaced by spaces (cx cy w h)
        # example: team5/dashboard/5:10 20 5 5
        # print('received:', msg.topic, msg.payload.decode())
        if msg.topic[len(topic_sub)-1:] in data.keys():
            sensor_type = msg.topic[len(topic_sub)-1:]
            payload = msg.payload.decode()
            # print("received:",sensor_type, payload)
            canvas.itemconfig(data[sensor_type]['data'], text=payload)
                
    
    client.subscribe(topic_sub)
    client.on_message = on_message


window = Tk()
window.title("MQTT Sensor Dashboard")
win_w = 160
win_h = 120
mult = 4
base = 50
window.geometry(str(win_w * mult)+"x"+str(win_h * mult+base))
window.resizable(False,False)
window.configure(bg="white")
canvas = Canvas(window, bg="white", width=win_w*mult,height=win_h*mult)
canvas.place(x=0,y=0)

data = {}
data['ir'] = {'text': canvas.create_text(win_w*mult/4, win_h*mult/4, text='IR Sensor: '),
              'data': canvas.create_text(win_w*mult/2, win_h*mult/4, text='N/A')}
data['sonar'] = {'text': canvas.create_text(win_w*mult/4, win_h*mult/2, text='Sonar Sensor: '),
                'data': canvas.create_text(win_w*mult/2, win_h*mult/2, text='N/A')}
data['imu'] = {'text': canvas.create_text(win_w*mult/4, win_h*mult/4*3, text='IMU Z Acceleration: '),
                'data': canvas.create_text(win_w*mult/2, win_h*mult/4*3, text='N/A')}

# Connect
client = connect_mqtt()
subscribe(client)
client.loop_start()


window.mainloop()
client.loop_stop()