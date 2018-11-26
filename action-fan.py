#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import requests
import paho.mqtt.client as mqtt
from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io

CONFIG_INI = "config.ini"

# If this skill is supposed to run on the satellite,
# please get this mqtt connection info from <config.ini>
# Hint: MQTT server is always running on the master device
MQTT_IP_ADDR = "106.51.127.129"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

class Fan(object):
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
        
    # --> Sub callback function, one per intent
    def fanTurnOn_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")
        
        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        publishcommand()

        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, "Fan Turned On", "")

    # More callback function goes here...

    # --> Master callback function, triggered everytime an intent is recognized
    def master_intent_callback(self,hermes, intent_message):
        coming_intent = intent_message.intent.intent_name
        if coming_intent == 'fanTurnOn':
            self.fanTurnOn_callback(hermes, intent_message)

        # more callback and if condition goes here...
    def publishcommand():
    
       #ip_address=findmqttaddr()
        client = mqtt.Client()
        client.connect(MQTT_IP_ADDR,1883)     #Ip address and port
        client.publish("home/living","L1O")     #gatewayUID


    # --> Register callback function and start MQTT
    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.master_intent_callback).start()

if __name__ == "__main__":
    Fan()
