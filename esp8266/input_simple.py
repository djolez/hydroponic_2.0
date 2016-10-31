import machine
import logging
import time
import micropython
micropython.alloc_emergency_exception_buf(100)

from device import Device
import common

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

value = -1

class InputSimple(Device):
    trigger_type = {}
    trigger_type['on'] = machine.Pin.IRQ_RISING
    trigger_type['off'] = machine.Pin.IRQ_FALLING
    trigger_type['any'] = machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING
    
    def __init__(self, pin, name='input_simple', trigger=None, is_analog=False, resolution=None):
        super().__init__(pin, Device.types['in'], name)
        self.is_analog = is_analog
        common.state_changed[self.name] = None

        if(is_analog):
            self.__pin_object = machine.ADC(pin)
            self.read_function = self.__pin_object.read
            self.old_value = None
            '''determines the offset needed to trigger an interrupt'''
            self.resolution = resolution if resolution else 10
        else:
            self.__pin_object = machine.Pin(pin, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)
            self.__pin_object.irq(trigger=trigger, handler=self.change)
            self.read_function = self.__pin_object.value

    def change(self, v):
        common.state_changed[self.name] = self

    '''
        used for analog devices since they don't have IRQ,
        it should should be called from main loop
    '''
    def update(self):
        new_value = self.read(False)
        if(self.old_value is None):
            self.old_value = new_value

        if(abs(self.old_value - new_value) >= self.resolution):
            self.old_value = new_value
            self.change(new_value)
        
    def read(self, send_msg=True):
        value = self.read_function()
        
        if(send_msg):
            self.read_return(value)
        return value


