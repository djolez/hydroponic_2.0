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
        self.sub_devices = {}
        for i, rom in enumerate(self.__ds_object.scan()):
            self.sub_devices[str(i)] = {
                    'name': rom,
                    'min_value': -55,
                    'max_value': 125
            }
        self.last_value = None

    def read(self, send_response=True):
        logger.debug('{} -- Trying to read value'.format(self))
        self.__ds_object.convert_temp()
        time.sleep_ms(750)
        self.last_value = {}
        for name, obj in self.sub_devices.items():
            self.last_value[name] = self.__ds_object.read_temp(obj['name'])
        
        if(send_response):
            super().read_response()
