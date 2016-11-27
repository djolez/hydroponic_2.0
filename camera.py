import picamera
import logging
from time import sleep
import datetime as dt
#from schedule import *

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    'resolution': (1920, 1080),
    'quality': 7
}

def take_picture(file_path='img/', name_prefix='image', date_format='%Y-%m-%d@%H:%M:%S', config=None):
    
    if not file_path.endswith('/'):
        file_path += '/'

    with picamera.PiCamera() as camera:
        current_config = config if config != None else DEFAULT_CONFIG
        
        for key, value in DEFAULT_CONFIG.items():
            #quality of the picture is set differently than other options
            if key != 'quality':
                setattr(camera, key, value)
            else:
                picture_quality = value


        for key, value in current_config.items():
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
