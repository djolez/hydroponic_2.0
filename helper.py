import paho.mqtt.client as mqtt

def make_mqtt_client(on_connect, on_msg):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_msg
    client.connect('127.0.0.1')
    client.loop_start()
    return client



