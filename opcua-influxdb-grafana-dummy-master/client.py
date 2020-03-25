from opcua import Client
import requests
import time


url_opc_ua = "opc.tcp://51.144.139.143:4840"
client = Client(url_opc_ua)
client.connect()
print("client connected")

prev_temp_value = None
prev_press_value = None
prev_timestamp_value = None

while True:
	temp = client.get_node("ns=2;i=2")
	temp_value = temp.get_value()

	press = client.get_node("ns=2;i=3")
	press_value = press.get_value()

	timestamp = client.get_node("ns=2;i=4")
	timestamp_value = timestamp.get_value()

	is_update = prev_temp_value != temp_value and prev_press_value != press_value 
	if is_update:
		prev_temp_value = temp_value
		prev_press_value = press_value
		prev_timestamp_value = timestamp_value
		print(temp_value, press_value, timestamp_value)

		print("It is time to send some values to influx")
		url_influx = "http://23.101.74.113:8086/write?db=opcua&precision=s"
		payload = 'master-tag,'
		payload += 'company=Yara,'
		payload += 'owner=Yann\ Von '
		payload += 'temperature=' + str(temp_value)
		payload += ',pressure=' + str(press_value)
		payload += ' ' + str(int(timestamp_value.timestamp()))
		print(payload)
		headers = {
		  'Content-Type': 'application/x-www-form-urlencoded'
		}
		response = requests.request("POST", url_influx, headers=headers, data=payload)
		print(response)
		print()
