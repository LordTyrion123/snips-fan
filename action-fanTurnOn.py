#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
import os
import time
#from pixels import pixels

CONFIG_INI = "config.ini"

# If this skill is supposed to run on the satellite,
# please get this mqtt connection info from <config.ini>
# Hint: MQTT server is always running on the master device
MQTT_IP_ADDR = "106.51.127.129"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

class fanTurnOn(object):
    """Class used to wrap action code with mqtt connection
        
        Please change the name refering to your application
    """

    def __init__(self):
        # get the configuration if needed
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except :
            self.config = None

        # start listening to MQTT
        self.start_blocking()
    def publishcommand(self, powerstatus):
       #ip_address=findmqttaddr()
        client = mqtt.Client()
        client.connect(MQTT_IP_ADDR,1883)     #Ip address and port
        print(powerstatus)
        if powerstatus.lower() == "on":
            client.publish("inTopic","0")     #gatewayUID
        else:
            client.publish("inTopic","1")     #gatewayUID
        
    def lightcommand(self):
        #pixels.think()
        time.sleep(4)
        #pixels.off()
     
    def musicCommand(self):
        time.sleep(3)
        cmd = 'mpg321 /home/pi/Music/Daft_Punk_-_Around_The_World_mp3.shmidt.net.mp3'
        os.system(cmd)
        
    # --> Sub callback function, one per intent
    def fanTurnOn_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")
        
        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        powerstatus = intent_message.slots.on.first().value
        self.publishcommand(powerstatus)
        
        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, "Fan Turned On", "")

    # More callback function goes here...
    def lightTurnOn_callback(self, hermes, intent_message):
        hermes.publish_end_session(intent_message.session_id, "")
        
        print '[Received] intent : {}'.format(intent_message.intent.intent_name)
        self.lightcommand()
        hermes.publish_start_session_notification(intent_message.site_id, "Light Turned On", "")
        
    def playMusic_callback(self, hermes, intent_message):
        hermes.publish_end_session(intent_message.session_id,"")
        
        hermes.publish_start_session_notification(intent_message.site_id, "Music Played", "")
        self.musicCommand()

    # --> Master callback function, triggered everytime an intent is recognized
    def master_intent_callback(self,hermes, intent_message):
        coming_intent = intent_message.intent.intent_name
        if coming_intent == 'fanTurnOn':
            print("Testing")
            self.fanTurnOn_callback(hermes, intent_message)
        elif coming_intent == 'lordtyrion96:fanTurnOn':
            print(intent_message.slots.on.first().value)
            self.fanTurnOn_callback(hermes, intent_message)
        elif coming_intent == 'lordtyrion96:playMusic':
            self.playMusic_callback(hermes, intent_message)
#        elif coming_intent == 'lordtyrion96:lightTurnOn':
#            print("Testing 3")          
#            self.lightTurnOn_callback(hermes, intent_message)

        # more callback and if condition goes here...



    # --> Register callback function and start MQTT
    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.master_intent_callback).start()

if __name__ == "__main__":
    fanTurnOn()
