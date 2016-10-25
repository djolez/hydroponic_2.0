import machine
import logging

import config

import mqtt_client

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Device:
    def __init__(self, pin, device_type, name):
        self.pin = pin
        self.device_type = device_type
        self.name = name
        pin_type = machine.Pin.OUT if device_type is 'out' else machine.Pin.IN
        self.pin_object = machine.Pin(pin, pin_type)

    def __setup_communication(self):
        self.mqtt_topic = '{}/device/{}'.format(config.CONFIG['client_id'], self.name)
        self.mqtt_client = mqtt_client.make(self.mqtt_topic)

    def __send_msg(self, payload):
        logger.debug('{} sending msg: '.format(self.name, payload))
        self.mqtt_client.publish(self.mqtt_topic, payload)
		
    def change_state(self, state):
        if(state is 'on'):
            self.pin_object.value(0)
        elif(state is 'off'):
            self.pin_object.value(1)

        logger.debug('Toggled device on pin: {}, state: {}'.format(self.pin, state))
