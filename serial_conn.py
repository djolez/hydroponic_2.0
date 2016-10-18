import serial
import logging

logger = logging.getLogger(__name__)

serial_conn = serial.Serial('/dev/ttyACM0', 9600)

def write(msg):
    serial_conn.write(bytearray(msg + '\n', encoding='utf-8'))
    logger.debug('Wrote {}'.format(msg))

#write('device/light/off')
