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
topic_sub = "theIlluminati/#" # the topic the client is subscribed to

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
               theIlluminati/tag#/attribute 
            and if so, will update the dashboard accordingly."""
        
        # get the topics
        topic = msg.topic.split('/')
        # check if the topic is in the correct format
        if topic_sub[0:-2] in topic and len(topic) == 3:
            # get the tag# and the attribute
            tagNum = topic[1]
            attribute = topic[2]
            
            # check if the tag with the given tag# has already been created or not
            if tagNum not in tags.keys():
                # create the tag
                tags[tagNum] = {}

            # set the tag's attribute
            tags[tagNum][attribute] = float(msg.payload.decode())

            # check if the tag has all 6 attributes (x, y, w, h, id) but doesn't have a graphical representation
            if len(tags[tagNum]) == 6:
                # create the graphical representation
                x, y, w, h, id = tags[tagNum]['x'], tags[tagNum]['y'], tags[tagNum]['w'], tags[tagNum]['h'], tags[tagNum]['id'] # get the attributes
                x1, y1, x2, y2 = (x-w/2) * mult, (y-h/2) * mult, (x+w/2) * mult, (y+h/2) * mult # calculate the rectangle coordinates, scaled
                tags[tagNum]['rect'] = canvas.create_rectangle(x1, y1, x2, y2, fill="black") # create the rectangle
                tags[tagNum]['text'] = canvas.create_text(x*mult, y*mult, text=str(int(id)), fill="white") # create the text with the id
            elif len(tags[tagNum]) > 6:
                # graphical representation already created, instead of recreating, update it
                x, y, w, h, id = tags[tagNum]['x'], tags[tagNum]['y'], tags[tagNum]['w'], tags[tagNum]['h'], tags[tagNum]['id'] # get the attributes
                x1, y1, x2, y2 = (x-w/2) * mult, (y-h/2) * mult, (x+w/2) * mult, (y+h/2) * mult # calculate the rectangle coordinates, scaled
                canvas.coords(tags[tagNum]['rect'], x1, y1, x2, y2) # update the rectangle coordinates
                canvas.coords(tags[tagNum]['text'], x*mult, y*mult) # update the id text coordinates

    client.subscribe(topic_sub)     # subscribe the client to the topic_sub
    client.on_message = on_message  # link on_message

# create a window
window = Tk()
window.title("MQTT Camera Dashboard")
win_w = 160 # max x value of the camera
win_h = 120 # max y value of the camera
mult = 4 # multiplier to make the GUI larger than the size of the camera dimensions
base = 50 # bottom bar for other information (not used)
window.geometry(str(win_w * mult)+"x"+str(win_h * mult+base)) # set window size (camera dimensions * multiplier + bar at bottom)
window.resizable(False,False)
window.configure(bg="white")

# create the canvas
canvas = Canvas(window, bg="white", width=win_w*mult,height=win_h*mult) # set to dimensions of camera scaled
canvas.place(x=0,y=0)

# create the grid lines
canvas.create_line(win_w*mult, 18*mult, 0, 18*mult)
canvas.create_line(win_w*mult, 50*mult, 0, 50*mult)
canvas.create_line(win_w*mult, 84*mult, 0, 84*mult)
canvas.create_line(158*mult, win_h*mult, 158*mult, 0)
canvas.create_line(126*mult, win_h*mult, 126*mult, 0)
canvas.create_line(94*mult, win_h*mult, 94*mult, 0)
canvas.create_line(62*mult, win_h*mult, 62*mult, 0)
canvas.create_line(30*mult, win_h*mult, 30*mult, 0)

# dict of all the tags the camera has seen
tags = {}

# Connect to the broker
client = connect_mqtt()
subscribe(client)
client.loop_start()

# set looping
window.mainloop()
client.loop_stop()