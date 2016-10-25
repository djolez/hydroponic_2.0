import sensor_implementation as sensors
import device_implementation as devices
import config
import mqtt_client

from time import sleep
import logging
import ujson

logger = logging.getLogger(__name__)

def on_message(topic, msg):
    logger.debug('Topic {}, received msg: {}'.format(topic, msg))
    try:
        data = ujson.loads(msg)
        if(data['action'] is 'reregister'):
            register()
        elif(data['entity'] is 'sensor'):
            sensors.handle_msg(data)
        elif(data['entity'] is 'device'):
            devices.handle_msg(data)
    except ValueError:
        print('Failed to parse msg: {}'.format(msg))

def register():
    data = {}
    data['action'] = 'module_on'
    data['sensors'] = []
    data['devices'] = []
    data['module_name'] = config.CONFIG['client_id']

    for name, sensor_object in sensors.sensors.items():
        data['sensors'].append({'name': name})

    for name, device_object in devices.devices.items():
        data['devices'].append({'name': name, 'device_type': device_object.device_type})

    client.publish('main-dispatcher', ujson.dumps(data))

client = None

def main():
    global client
    client = mqtt_client.make(config.CONFIG['client_id'])
    #client = MQTTClient(config.CONFIG['client_id'], config.CONFIG['broker'])
    client.connect()
    client.set_callback(on_message)
    client.subscribe(config.CONFIG['client_id'])

    register()

    while True:
        client.check_msg()
        sleep(1)

main()
