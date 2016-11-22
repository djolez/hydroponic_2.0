import machine
import logging

from device import Device

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class OutputSimple(Device):

    #is_reverse True is used for relay since
    #0 means on and 1 means off
    def __init__(self, pin, name='output_simple', is_reverse=False, pwm_enabled=False):
        super().__init__(pin, Device.types['out'], name)
        
        self.__pin_object = machine.Pin(pin, machine.Pin.OUT)
        self.min_value = 0
        self.max_value = 1
        self.is_reverse = is_reverse
        self.pwm_enabled = pwm_enabled 
        if(pwm_enabled):
            self.__pwm_object = machine.PWM(self.__pin_object, freq=1000)
            self.max_value = 1023
        self.last_value = None

    def read(self, send_response=True):
        self.last_value = self.__pin_object.value()

        if(send_response):
            super().read_response()
    
    def write(self, value):
        if(self.pwm_enabled):
            print('here')
            self.__pwm_object.duty(value)
            return
        if(self.is_reverse):
            value = 1 if value == 0 else 0
         
        self.__pin_object.value(value)

