import logging
import datetime as dt
import json

import helper

logger = logging.getLogger(__name__)

class Sensor:

    def __init__(self, name, parent_module_name): 
        self.name = name
        self.parent_module_name = parent_module_name
        self.__mqtt_client = helper.make_mqtt_client(self.__on_mqtt_connect, self.__on_mqtt_message)

        logger.debug('{} -- Initialized'.format(self)) 

    def __str__(self):
        return '[name: {}, parent: {}]'.format(self.name, self.parent_module_name)

    def __del__(self):
        logger.debug('{} -- Deleting instance'.format(self))
        self.__mqtt_client.loop_stop()

    def release(self):
        self.__mqtt_client.loop_stop()

    def read(self):
        self.__send_message({'action': 'read'})
    
    def __on_mqtt_connect(self, client, userdata, flags, rc):
        logger.debug('{} -- MQTT connection established'.format(self))
        
        client.subscribe('{}/sensor/{}/#'.format(self.parent_module_name, self.name))

    def __on_mqtt_message(self, client, usrdata, msg):
        logger.debug('{} -- Received message -- {}'.format(self, msg.payload))
    
    def __send_message(self, msg):
        logger.debug('{} -- Sending message "{}"'.format(self, msg))
        msg['entity'] = 'sensor'
        msg['name'] = self.name
        self.__mqtt_client.publish('{}'.format(self.parent_module_name), json.dumps(msg))
