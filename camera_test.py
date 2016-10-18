import camera
import logging
from time import sleep

logging.basicConfig(level = logging.DEBUG, format='%(asctime)s %(name)s - %(levelname)s\n   %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
logger = logging.getLogger(__name__)

camera.take_picture('img')

def check():
    return True

#camera.start_timelapse(5, 'img/timelapse', 'timelapse', check)

#sleep(8)
#camera.__loop_timelapse(5, 'img/timelapse', 'timelapse', check)

#sleep(12)
#camera.stop_timelapse()

while True:
    a = 1
