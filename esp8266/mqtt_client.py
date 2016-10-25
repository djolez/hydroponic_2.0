from umqtt_simple import MQTTClient

import config
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def make(topic):
    client = MQTTClient(topic, config.CONFIG['broker'])
    client.connect()
    logger.debug("Established connection to {}".format(topic))
    return client
