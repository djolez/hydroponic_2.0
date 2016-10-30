import machine
import logging
import time
import micropython
micropython.alloc_emergency_exception_buf(100)

from device import Device
import helper

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

value = -1

class InputSimple(Device):

    def __init__(self, pin, name, trigger, is_analog=False):
        super().__init__(pin, Device.types['in'], name)
        self.is_analog = is_analog

        if(is_analog):
            self.__pin_object = machine.ADC(pin)
        else:
            self.__pin_object = machine.Pin(pin, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)
            self.__pin_object.irq(trigger=trigger, handler=self.change)

    def change(self, v):
        helper.state_changed = self.name

    def read(self):
        value = None
        if(self.is_analog):
            value = self.__pin_object.read()
        else:
            value = self.__pin_object.value()
        self.read_return(value)
        return value


