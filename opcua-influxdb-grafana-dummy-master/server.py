from datetime import datetime
from opcua import Server
from random import randint
import time


server = Server()

url = "opc.tcp://127.0.0.1:4840"
server.set_endpoint(url)

name = "OPCUA_DUMMY_SIMULATION_SERVER"
addspace = server.register_namespace(name)

node = server.get_objects_node()

param =	node.add_object(addspace, "Parameters")

temp = param.add_variable(addspace, "Temperature", 0)
press = param.add_variable(addspace, "Pressure", 0)
timestamp = param.add_variable(addspace, "Timestamp", 0)

temp.set_writable()
press.set_writable()
timestamp.set_writable()

server.start()
print("Server started at {}".format(url))

while True:
	temp_value = randint(10, 50)
	press_value = randint(200, 999)
	timestamp_value = datetime.now()

	print(temp_value, press_value, timestamp_value)

	temp.set_value(temp_value)
	press.set_value(press_value)
	timestamp.set_value(timestamp_value)

	time.sleep(2.0)
