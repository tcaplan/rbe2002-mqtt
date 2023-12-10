from tkinter import *
from paho.mqtt import client as mqtt_client
import json
import os
from dotenv import load_dotenv

# load the env variables
load_dotenv()

# get environment variables for connecting to the MQTT server
broker = os.getenv('MQTT_SERVER')
port = int(os.getenv('MQTT_PORT'))
username = os.getenv('MQTT_USER')
password = os.getenv('MQTT_PASS')

topic = "team5" # the topic the client will publish to
topic_sub = "team5/sensors/#" # the topic the client is subscribed to

def connect_mqtt():
    """Function creates a client that has attempted to connect to the broker and returns it."""
    def on_connect(client, userdata, flags, rc):
        """Prints if the connection was successful, otherwise will print the failed return code."""
        if rc==0:
            print("Successfully connected to MQTT broker")
        else:
            print("Failed to connect, return code %d", rc)


    client = mqtt_client.Client(protocol=mqtt_client.MQTTv311)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    '''subscribes the given client to the topic_sub'''
    def on_message(client, userdata, msg):
        """When receiving a message of the topic_sub, checks in the proper format:
               team5/sensors/sensor_type 
            and if so, will update the dashboard accordingly."""
        if msg.topic[len(topic_sub)-1:] in data.keys():
            sensor_type = msg.topic[len(topic_sub)-1:] # get the sensor_type
            payload = msg.payload.decode() # get the data
            canvas.itemconfig(data[sensor_type]['data'], text=payload) # set the text for the given sensor to the new data
                
    
    client.subscribe(topic_sub)     # subscribe the client to the topic_sub
    client.on_message = on_message  # link on_message

# create a window
window = Tk()
window.title("MQTT Sensor Dashboard")
win_w = 160 # max x value of the camera
win_h = 120 # max y value of the camera
mult = 4 # multiplier to make the GUI larger than the size of the camera dimensions
base = 50 # bottom bar for other information (not used)
window.geometry(str(win_w * mult)+"x"+str(win_h * mult+base)) # set window size (camera dimensions * multiplier + bar at bottom)
window.resizable(False,False)
window.configure(bg="white")

# create the canvas
canvas = Canvas(window, bg="white", width=win_w*mult,height=win_h*mult)
canvas.place(x=0,y=0)

# dict of all sensors and their corresponding graphics
data = {}

# add the sensors to the GUI with labels and N/A readings to start
data['ir'] = {'text': canvas.create_text(win_w*mult/4, win_h*mult/4, text='IR Sensor: '),
              'data': canvas.create_text(win_w*mult/2, win_h*mult/4, text='N/A')}
data['sonar'] = {'text': canvas.create_text(win_w*mult/4, win_h*mult/2, text='Sonar Sensor: '),
                'data': canvas.create_text(win_w*mult/2, win_h*mult/2, text='N/A')}
data['imu'] = {'text': canvas.create_text(win_w*mult/4, win_h*mult/4*3, text='IMU Z Acceleration: '),
                'data': canvas.create_text(win_w*mult/2, win_h*mult/4*3, text='N/A')}

# Connect to the broker
client = connect_mqtt()
subscribe(client)
client.loop_start()

# set looping
window.mainloop()
client.loop_stop()