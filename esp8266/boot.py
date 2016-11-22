import network
import webrepl

ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

def wifi_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('...', '...')
        while not sta_if.isconnected():
            pass
	webrepl.start(password='...')
    print('network config:', sta_if.ifconfig())
	
wifi_connect()

