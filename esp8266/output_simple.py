import machine
import logging

from device import Device

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class OutputSimple(Device):

    #is_reverse True is used for relay since
    #0 means on and 1 means off
    def __init__(self, pin, is_reverse=False):
        super().__init__(pin, Device.types['out'], 'relay')
        
        self.__pin_object = machine.Pin(pin, machine.Pin.OUT)
        self.is_reverse = is_reverse

    def read(self):
        res = self.__pin_object.value()

        super().read_return(res)
    
    def write(self, value):
        write_value = -1
        
        if(value is 'on'):
            write_value = 0 if self.is_reverse else 1
        elif(value is 'off'):
            write_value = 1 if self.is_reverse else 0
        
        if(write_value == -1):
            logger.error('{} -- An error has occured while trying to write value'.format(self))
            return
        self.__pin_object.value(write_value)
