import datetime as dt

from classes.schedule import *

class Action:

    def __init__(self, name, time=None, repeat=None, callbacks=[], force_execute=False):
        '''
            By setting the time attribute action is executed every repeat period

            By setting only the repeat attribute action is executed every n days/hours/minutes/seconds
        '''
        self.name = name
        self.time = time
        self.repeat = repeat
        self.callbacks = callbacks
        self.force_execute = force_execute
        self.scheduler_object = None
    
        #atexit.register(self.deschedule)

    def __str__(self):
        return '[action: {} @ {}]'.format(self.name, self.time or self.repeat)

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

        logger.debug('{} -- Scheduled'.format(self))

    def deschedule(self):
        if(self.scheduler_object is not None):
            self.scheduler_object.stop()

    def execute(self, forced=False):
        for c in self.callbacks:
            c()
        if not forced:
            self.schedule()

