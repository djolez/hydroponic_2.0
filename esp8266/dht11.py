import dht
import machine
import logging

from device import Device

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Dht11(Device):

    def __init__(self, pin, name='dht11'):
        super().__init__(pin, Device.types['in'], name)
        
        self.__pin_object = machine.Pin(pin)
        self.__dht_object = dht.DHT11(self.__pin_object)
        self.is_multiple = True
        self.sub_devices = {
                'temperature': {
                    'min_value': 0,
                    'max_value': 50
                },
                'humidity': {
                    'min_value': 20,
                    'max_value': 80
                },

        }
        self.last_value = {}

    def read(self, send_response=True):
        logger.debug('{} -- Trying to read value'.format(self))
        self.__dht_object.measure()
        self.last_value['temperature'] = self.__dht_object.temperature()
        self.last_value['humidity'] = self.__dht_object.humidity()

        if(send_response):
            super().read_response()
