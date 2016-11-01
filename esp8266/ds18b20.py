import ds18x20
import onewire
import machine
import time
import logging

from device import Device

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Ds18b20(Device):

    def __init__(self, pin, name='ds18b20'):
        super().__init__(pin, Device.types['in'], name)
        
        self.__pin_object = machine.Pin(pin)
        self.__ds_object = ds18x20.DS18X20(onewire.OneWire(self.__pin_object))
        self.__ds_instance = self.__ds_object.scan()[0]
        self.last_value = None

    def read(self, send_response=True):
        logger.debug('{} -- Trying to read value'.format(self))
        self.__ds_object.convert_temp()
        time.sleep_ms(750)
        self.last_value = self.__ds_object.read_temp(self.__ds_instance)
        
        if(send_response):
            super().read_response()
