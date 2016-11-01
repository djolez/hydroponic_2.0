import logging
import copy
import sys

from sensor import *
from device import *

logger = logging.getLogger(__name__)

class Module:

    def __init__(self, name, devices):
        if(devices is None):
            devices = []

        self.name = name
        self.devices = {}

        for d in devices:
            self.add_device(Device(d['name'], d['device_type'], self.name))

    def __str__(self):
        return '[name: {}]'.format(self.name)

    def __del__(self):
        logger.debug('{} -- Deleting instance'.format(self))

        for d in self.devices:
            d.close_connection()

    def add_device(self, d):
        self.devices[d.name] = d
