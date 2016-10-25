from sensor import Sensor

import dht
import onewire
import ds18x20
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def handle_msg(msg):
    if(msg['action'] is 'read'):
        sensors[msg['name']].read()

def init_dht(self):
    self.instance = dht.DHT11(self.pin_object)		

def read_dht(self):
    self.instance.measure()
    return {'TEMP': self.instance.temperature(), 'HUMIDITY': self.instance.humidity()}

def read_simple(self):
    return self.pin_object.read()

def init_water_temp(self):
    self.additional = ds18x20.DS18X20(onewire.OneWire(self.pin_object))
    self.instance = self.additional.scan()[0]

def read_water_temp(self):
    self.additional.convert_temp()
    time.sleep_ms(750)
    return self.additional.read_temp(self.instance)

def init():
    dht = Sensor('TEMP_HUMIDITY', 1, init_func=init_dht, read_func=read_dht)
    light = Sensor('LIGHT', 0, read_func=read_simple, is_analog=True)
    water_temp = Sensor('WATER_TEMP', 10, init_func=init_water_temp, read_func=read_water_temp)

    global sensors
    sensors = {}
    sensors['TEMP_HUMIDITY'] = dht
    sensors['LIGHT'] = light
    sensors['WATER_TEMP'] = water_temp

init()
