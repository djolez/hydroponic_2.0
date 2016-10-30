import logging
import micropython
micropython.alloc_emergency_exception_buf(100)

import config
import mqtt_client

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Device:
    types = { 'in': 1, 'out': 2 }

    def __init__(self, pin, device_type, name):
        self.pin = pin
        self.device_type = device_type
        self.name = '{}_{}'.format(name, pin)
        self.__setup_communication()
        
        logger.debug('{} -- Initialized'.format(self))

    def __str__(self):
        return '[name: {}]'.format(self.name)

    def __setup_communication(self):
        self.__mqtt_topic = '{}/device/{}'.format(config.CONFIG['client_id'], self.name)
        self.__mqtt_client = mqtt_client.make(self.__mqtt_topic)

    def __send_msg(self, payload):
        logger.debug('{} -- Sending msg: {}'.format(self, payload))
        self.__mqtt_client.publish(self.__mqtt_topic, payload)

    def read(self):
        raise NotImplementedError

    def read_return(self, value):
        self.__send_msg(b"{{ 'action': 'result', 'value': {} }}".format(value))

    def write(self):
        raise NotImplementedError

    def interrupt(self, value):
        self.__send_msg(b"{{ 'action': 'interrupt', 'value': {} }}".format(value))
