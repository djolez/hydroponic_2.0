import logging
import ujson

logger = logging.getLogger(__name__)

CONFIG = {
    "broker": "192.168.1.3",
    "client_id": "esp8266"
}

def read():
    try:
        global CONFIG
        with open('config.json', 'r') as f:
            print(f.read())
            CONFIG = ujson.loads(f.read())
    except OSError:
        logger.error('File config.json not found')
    except ValueError as e:
        logger.error('Failed to parse config.json {}'.format(e))

if CONFIG is None:		
    read()
