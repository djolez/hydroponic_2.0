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

    def __send_msg(self, subtopic, payload):
        logger.debug('{} -- Sending msg: {}'.format(self, payload))
        self.__mqtt_client.publish('{}/{}'.format(self.__mqtt_topic, subtopic), payload)

    def read(self):
        raise NotImplementedError

    def read_response(self):
        self.__send_msg('read-response', b"{{ 'value': {} }}".format(self.last_value))

    def write(self):
        raise NotImplementedError

    def interrupt(self):
        self.__send_msg('interrupt', b"{{ 'value': {} }}".format(self.last_value))
