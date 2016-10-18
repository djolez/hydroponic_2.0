import picamera
import logging
from time import sleep
import datetime as dt
from schedule import *

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    'resolution': (1920, 1080),
    'quality': 7
}

def take_picture(file_path, name_prefix='image', date_format='%Y-%m-%d@%H:%M:%S', config=None):
    
    if not file_path.endswith('/'):
        file_path += '/'

    with picamera.PiCamera() as camera:
        current_config = config if config != None else DEFAULT_CONFIG
        
        for key, value in current_config.iteritems():
            #quality of the picture is set differently than other options
            if key != 'quality':
                setattr(camera, key, value)
            else:
                picture_quality = value

        #give camera enough time to auto adjust
        sleep(2)
        
        try:
            now = dt.datetime.now()
            file_name = name_prefix + (now.strftime(date_format)) + '.jpg'
        except ValueError as e:
            logger.exception('Wrong date format specified')
        
        try:
            logger.debug('Taking picture {}'.format(file_path + file_name))
            camera.capture(file_path + file_name, quality = picture_quality)
            return file_name
        except Exception as e:
            logger.exception('There was an exception while taking the picture')

next_timelapse_schedule_obj = None

def __loop_timelapse(interval_in_sec, file_path, name_prefix, check_func):
    
    if(check_func != None):
        if(check_func()):
            take_picture(file_path, name_prefix)
    else:
        take_picture(file_path, name_prefix)

    next_time = dt.datetime.now() + dt.timedelta(seconds=interval_in_sec)
    
    global next_timelapse_schedule_obj
    next_timelapse_schedule_obj = Schedule('timelapse_photo', next_time, __loop_timelapse, [interval_in_sec, file_path, name_prefix, check_func])


#check_func is a callback function that returns
#a boolean whether a pic should be taken or not
def start_timelapse(interval_in_sec, file_path, name_prefix='timelapse', check_func=None):
    __loop_timelapse(interval_in_sec, file_path, name_prefix, check_func)

def stop_timelapse():
    global next_timelapse_schedule_obj
    if next_timelapse_schedule_obj != None:
        next_timelapse_schedule_obj.stop()
        next_timelapse_schedule_obj = None





