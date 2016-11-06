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

    def __init__(self, pin, name='input_simple', trigger=None, is_analog=False, resolution=None, debounce_time=0):
        super().__init__(pin, Device.types['in'], name)
        self.is_analog = is_analog
        common.state_changed[self.name] = None
        self.last_value = None
        self.last_read_time = None
        self.debounce_time = debounce_time

        if(is_analog):
            self.__pin_object = machine.ADC(pin)
            self.read_function = self.__pin_object.read
            '''determines the offset needed to trigger an interrupt'''
            self.resolution = resolution if resolution else 10
        else:
            self.__pin_object = machine.Pin(pin, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)
            self.__pin_object.irq(trigger=trigger, handler=self.change)
            self.read_function = self.__pin_object.value

    def change(self, v):
        '''debounce input'''
        if(self.last_read_time is not None and time.ticks_diff(self.last_read_time, time.ticks_ms()) < self.debounce_time):
            return
        self.read(False)

        common.state_changed[self.name] = self

    '''
        used for analog devices since they don't have IRQ,
        it should should be called from main loop
    '''
    def update(self):
        old_value = self.last_value
        self.read(False)
        if(old_value is None):
            old_value = self.last_value

        if(abs(old_value - self.last_value) >= self.resolution):
            self.change(self.last_value)
    
    def read(self, send_response=True):
        value = self.read_function()
        self.last_value = value
        self.last_read_time = time.ticks_ms()

        if(send_response):
            self.read_response()
        return value


