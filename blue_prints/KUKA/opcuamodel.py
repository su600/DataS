import asyncio
import copy
import logging
from datetime import datetime
import time
from math import sin
import sys
sys.path.insert(0, "..")


logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')


from asyncua import ua, uamethod, Server

# from tests.test_common import *

@uamethod
def func(parent, value):
    return value * 2


class SubHandler(object):

    """
    Subscription Handler. To receive events from server for a subscription
    """

    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node, val)

    def event_notification(self, event):
        print("Python: New event", event)



async def main():
    # setup our server
    server = Server()
    await server.init()
    server.set_endpoint('opc.tcp://0.0.0.0:4840')
    # server.set_endpoint('opc.tcp://192.168.100.170:4840')
    # setup our own namespace, not really necessary but should as spec
    server.set_server_name("SU OPC UA Server read test")
    # server.set_security_policy([
    #     ua.SecurityPolicyType.NoSecurity,
    #     ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
    #     ua.SecurityPolicyType.Basic256Sha256_Sign])

    uri = 'http://examples.freeopcua.github.io'
    idx = await server.register_namespace(uri)

    await server.import_xml('www.xml')
    # # get Objects node, this is where we should put our nodes
    objects = server.get_objects_node()

    # todo 对于变量固定的 适合用xml生成信息模型
    # kukaobj1=await objects.add_object(idx,'KUKA_ROBOT_1')
    # kukafloder1=await kukaobj1.add_folder(idx,'Axis')
    # kukavar1 = kukafloder1.add_variable()
    # kukavar2 = kukafloder1.add_variable()
    # kukavar3 = kukafloder1.add_variable()
    # kukavar4 = kukafloder1.add_variable()
    # kukavar5 = kukafloder1.add_variable()
    # kukavar6 = kukafloder1.add_variable()
    # kukafloder2 = await kukaobj1.add_folder(idx, 'Degree')
    # kukavar7 = kukafloder2.add_variable()
    # kukavar8 = kukafloder1.add_variable()
    # kukavar9 = kukafloder1.add_variable()
    # kukavar10 = kukafloder1.add_variable()
    # kukavar11 = kukafloder1.add_variable()
    # kukavar12 = kukafloder1.add_variable()

    # myobj = await objects.add_object(idx, 'MyObject')
    # myvar = await myobj.add_variable(idx, 'MyVariable', 6.7)
    # # Set MyVariable to be writable by clients
    # await myvar.set_writable()
    # await objects.add_method(
    #     ua.NodeId('ServerMethod', 2), ua.QualifiedName('ServerMethod', 2),
    #     func, [ua.VariantType.Int64], [ua.VariantType.Int64]
    # )
    _logger.info('Starting server!')
    async with server:
        count = 0
        while True:
            await asyncio.sleep(1)
            count += 0.1
            # _logger.info('Set value of %s to %.1f', myvar, count)
            # await myvar.write_value(count)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    # loop.set_debug(True)
    loop.run_until_complete(main())
