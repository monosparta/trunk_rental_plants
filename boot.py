import gc
import network
import esp

from errorlog import ErrorLogger

esp.osdebug(None)
gc.collect()

# wifi list
wifi_list = [
    {'ssid': 'monospace', 'password': '22012870'},
    {'ssid': 'TrunkStudio-2.4G', 'password': '22019020'}
]

station = network.WLAN(network.STA_IF)

station.active(True)

points = station.scan()

connected = False

for wifi in wifi_list:
    print(f"Trying to find wifi {wifi['ssid']}")
    if any(elem[0].decode("utf-8") == wifi['ssid'] for elem in points):
        print(f"{wifi['ssid']} found, Connecting...")
        station.connect(wifi['ssid'], wifi['password'])

        while station.isconnected() == False:
            pass
        connected = True
        break

if connected:
    print('Connection successful')
    print(station.ifconfig())
else:
    print('No connection available!')
    error_logger = ErrorLogger()
    error_times = error_logger.add_error('WiFi connection error')
    error_logger.retry(error_times);
