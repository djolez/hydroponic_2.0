import logging
import copy
import sys

from sensor import *

logger = logging.getLogger(__name__)

class Module:

    def __init__(self, name, sensors=None, devices=None):
        if(sensors is None):
            sensors = []
        if(devices is None):
            devices = []

        self.name = name
        self.sensors = []

        for s in sensors:
            self.sensors.append(Sensor(s['name'], self.name))
        
        for d in devices:
            self.devices.append(Device(d['name'], d['device_type'], self.name))

    def __str__(self):
        return '[name: {}]'.format(self.name)

    def __del__(self):
        logger.debug('{} -- Deleting instance'.format(self))
        
        for s in self.sensors:
            #because __del__ is not called(there are other references left, i don't know form where)
            s.release()

