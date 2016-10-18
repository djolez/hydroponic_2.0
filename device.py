import logging
import datetime as dt
#import serial_conn
import atexit
from blinker import signal

from schedule import *
from time_module import *
import helper

logger = logging.getLogger(__name__)


class Device:

    def __init__(self, name, device_type, parent_module_name): 
        self.name = name
        self.device_type = device_type
        self.parent_module_name = parent_module_name
        #used for subscribing to device on/off actions
        self.on_event = signal(self.name + '_on')
        self.off_event = signal(self.name + '_off')
        
        self.__mqtt_client = helper.make_mqtt_client(self.__on_mqtt_connect, self.__on_mqtt_message)

        logger.debug('{} -- Initialized'.format(self)) 
    
    def __str__(self):
        return '[name: {}]'.format(self.name)
    
    def __on_mqtt_connect(self, client, userdata, flags, rc):
        logger.debug('{} -- MQTT connection established'.format(self))
        
        client.subscribe('{}/device/{}/#'.format(self.parent_module_name, self.name))

    def __on_mqtt_message(self, client, usrdata, msg):
        logger.debug('{} -- Received message -- {}'.format(self, msg.payload))

    def __send_message(self, msg):
        logger.debug('Sending message "{}" for {}'.format(msg, self.name))
        self.__mqtt_client.publish('device/real/{}'.format(self.name), msg)

    def on(self, args=None):
        self.__send_message('on')
        self.on_event.send()

    def off(self, args=None):
        self.__send_message('off')
        self.off_event.send()

class Action:

    def __init__(self, name, time=None, repeat=None, callbacks=[], force_execute=False):
        """
            By setting the time attribute action is executed every repeat period

            By setting only the repeat attribute action is executed every n days/hours/minutes/seconds
        """
        self.name = name
        self.time = time
        self.repeat = repeat
        self.callbacks = callbacks
        self.force_execute = force_execute
        self.scheduler_object = None
    
        #atexit.register(self.deschedule)

    def __str__(self):
        return '[action: {} @ {}]'.format(self.name, self.time)

    def schedule(self):
        
        if(self.time is not None):
            time = self.time.to_date()
            now = dt.datetime.now()
            
            if(time < now):
                if(self.force_execute):
                    self.execute(True)
                time += dt.timedelta(days=1)
        if(self.repeat is not None):
            if(self.force_execute):
                self.force_execute = False
                self.execute(True)
            now = dt.datetime.now()
            time = now + dt.timedelta(seconds=self.repeat.to_seconds())
        
        self.scheduler_object = Schedule(self.name, time, self.execute)

    def deschedule(self):
        if(self.scheduler_object is not None):
            self.scheduler_object.stop()

    def execute(self, forced=False):
        for c in self.callbacks:
            c()
        if not forced:
            self.schedule()





