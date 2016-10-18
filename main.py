from device import *
import datetime as dt
import logging
import sys
import camera

logging.basicConfig(level = logging.DEBUG, format='%(asctime)s %(name)s - %(levelname)s\n   %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
logger = logging.getLogger(__name__)

#if(len(sys.argv) == 1):
#    logger.error('Serial port arg not found, stopping')
#    raise SystemExit(0)

#serial_conn = serial.Serial('/dev/{}'.format(sys.argv[1]), 9600)

on = dt.datetime.now() + dt.timedelta(seconds=5)
off = on + dt.timedelta(minutes=10)

on_a = off + dt.timedelta(seconds=5)
off_a = on_a + dt.timedelta(seconds=10)



pump = Device('pump', [
        Action((7, 30), 'on'),
        Action((7, 40), 'off'),
        
        Action((14, 0), 'on'),
        Action((14, 10), 'off'),
        
        Action((21, 0), 'on'),
        Action((21, 10), 'off'),

        """{
            'time': Time(7, 30),
            'action': 'on'
        },
        {
            'time': Time(7, 40),
            'action': 'off'
        },
        {
            'time': Time(14, 0),
            'action': 'on'
        },
        {
            'time': Time(14, 10),
            'action': 'off'
        },
        {
            'time': Time(21, 0),
            'action': 'on'
        },
        {
            'time': Time(21, 10),
            'action': 'off'
        }"""
    ])

pump.enable()

light = Device('light', [
        Action((7, 0), 'on', True),
        Action((1, 0), 'off'),
         
        """{
            'time': Time(7, 0),
            'action': 'on',
            'force': True
        },
        {
            'time': Time(1, 0),
            'action': 'off'
        }"""
   ])

light.enable()

def is_daylight():
    now = dt.datetime.now()
    start = now.replace(hour=7, minute=0, second=0)
    end = (now + dt.timedelta(days=1)).replace(hour=1, minute=0, second=0)
    if(start < now < end):
        return True
    else:
        return False

camera.start_timelapse(15*60, '/home/djolez/hydroponic/web-app/img/timelapse', check_func=is_daylight)

while(True):
    a = 1

