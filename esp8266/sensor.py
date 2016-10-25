#import mqtt_client

import machine
import logging
import config
import mqtt_client

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Sensor:
    def __init__(self, name, pin, read_func, init_func=None, is_analog=False):
        self.name = name
	self.pin = pin
        self.pin_object = machine.Pin(pin) if not is_analog else machine.ADC(pin)
        self.read_func = read_func
        self.init_func = init_func
        self.mqtt_client = None
		
        if(self.init_func):
            self.init_func(self)
            logger.debug('Initialized {}'.format(self))
		
            self.__setup_communication()
		
    def __str__(self):
        return '[name: {}, pin: {}]'.format(self.name, self.pin)
	
    def __setup_communication(self):
        self.mqtt_topic = '{}/sensor/{}'.format(config.CONFIG['client_id'], self.name)
        self.mqtt_client = mqtt_client.make(self.mqtt_topic)
		
    def __send_msg(self, payload):
        logger.debug('{} sending msg: '.format(self.name, payload))
        self.mqtt_client.publish(self.mqtt_topic, payload)
    
    def read(self, send_response=True):
        result = self.read_func(self)
		
        if(send_response):
            msg = b'{{"action": "result", "value": {} }}'.format(result)
            self.__send_msg(msg)
        return result
