import logging
import datetime as dt
import atexit
from blinker import signal
import json
import collections

from schedule import *
from time_module import *
import helper

logger = logging.getLogger(__name__)


class Device:
    types = { 'in': 1, 'out': 2 }

    def __init__(self, name, device_type, parent_module_name, sub_devices): 
        self.name = name
        self.device_type = device_type
        self.parent_module_name = parent_module_name
        self.sub_devices = sub_devices
        self.is_multi_device = sub_devices is not None
        self.last_value = None
        
        '''used for subscribing to device events'''
        self.on_event = signal(self.name + '_on')
        self.off_event = signal(self.name + '_off')
        if(device_type == Device.types['in']):
            self.interrupt_event = signal(self.name + '_interrupt')
            self.value_low = signal(self.name + '_value_low')
            self.value_high = signal(self.name + '_value_high')

        self.__mqtt_client = helper.make_mqtt_client(self.__on_mqtt_connect, self.__on_mqtt_message)

        logger.debug('{} -- Initialized'.format(self)) 
    
    def __str__(self):
        return '[name: {}]'.format(self.name)
    
    def __on_mqtt_connect(self, client, userdata, flags, rc):
        logger.debug('{} -- MQTT connection established'.format(self))
        topic = '{}/device/{}'.format(self.parent_module_name, self.name) 
        client.subscribe(topic + '/#')
        client.message_callback_add(topic + '/read-response/#', self.read_response)
        client.message_callback_add(topic + '/interrupt/#', self.interrupt)
        
    def __on_mqtt_message(self, client, usrdata, msg):
        logger.debug('{} -- Received message -- {}'.format(self, msg.topic))

    def close_connection(self):
        self.__mqtt_client.disconnect()
    
    def __send_message(self, msg):
        '''logger.debug('{} -- Sending message "{}"'.format(self, msg))'''
        msg['name'] = self.name
        self.__mqtt_client.publish('{}'.format(self.parent_module_name), json.dumps(msg))

    def read(self):
        self.__send_message({'action': 'read'})
    
    OUTPUT_WIDTH = 50
    OUTPUT_VAL_FIELD_SIZE = 4
    '''def log_sensor_data(self, name, value, logger = logger.INFO):
        
        diff = self.OUTPUT_WIDTH - len(name) - self.OUTPUT_VAL_FIELD_SIZE
        logger('{} ' + ('-' * diff) + ' {}').format(name, value))
    '''

    def read_response(self, client, usrdata, msg):
        data = json.loads(msg.payload.decode('utf-8'))
        logger.debug('{} -- read_response -- {}'.format(self, data))

        for sensor_name, sub_values in data.items():
            '''bottom_line = '|' + ('_' * (len(sensor_name) + 2)) + '|'
            logger.info('| {} |\n{}'.format(sensor_name, bottom_line))'''
            
            for n, v in sub_values.items():
                v = round(v, 2)  
                #self.log_sensor_data(n, v)

                if(n == '0'):
                    logger.info('{} -------- {}'.format('bottom', v))
                if(n == '1'):
                    logger.info('{} ------- {}'.format('ambient', v))
                if (n == 'humidity'):
                    logger.info('{} ------ {}'.format(n, v))
                if (n == 'temperature'):
                    logger.info('{} ----------- {}'.format('mid', v))

                logger.info('')

        '''>>>>>if(n is '0' or name is '1'):
                    logger.info('\t\t{}: \t{}'.format(n, v))
                else:
                    logger.info('\t\t{}: \t\t{}'.format(n, v))
                '''

        '''>>>>>for name, obj in data.items():
            if(self.is_multi_device):
                for n, v in obj.items():
                    if(v < self.sub_devices[n]['desired_min_value']):
                        self.value_low.send()
                    if(v > self.sub_devices[n]['desired_max_value']):
                        self.value_high.send()'''

    def write(self, value):
        self.__send_message({'action': 'write', 'value': value})

    def interrupt(self, client, usrdata, msg):
        logger.debug('{} -- interrupt -- {}'.format(self, msg.payload))
        data = json.loads(msg.payload.decode('utf-8'))
        self.last_value = data[self.name]
        self.interrupt_event.send()

