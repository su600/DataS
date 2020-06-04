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

    await server.import_xml('kuka.xml')
    ## get Objects node, this is where we should put our nodes
    # await server.start()

    # root = server.get_root_node()
    # # _logger.info("Root node is: %r", root)
    # objects = server.get_objects_node()
    # # _logger.info("Objects node is: %r", objects)
    # # print(server.get_namespace_index())
    # # myvar = await root.get_child(["0:Objects","3:KUKA_1",'0:x'])
    # # bo=await objects.get_children()
    # myvar = await objects.get_children()
    # # myvar.
    # # myvar(['0:actuator1'])
    # print(myvar)

    # root = server.get_root_node()
    # actuator1 = await root.get_child(["0:Objects", "0:Actuator", '0:actuator1'])
    # actuator2 = await root.get_child(["0:Objects", "0:Actuator", '0:actuator2'])
    # actuator3 = await root.get_child(["0:Objects", "0:Actuator", '0:actuator3'])
    # actuator4 = await root.get_child(["0:Objects", "0:Actuator", '0:actuator4'])
    # degree1 = await root.get_child(["0:Objects", "0:Drulling_Robot", '0:Degree', '0:degree1'])
    # degree2 = await root.get_child(["0:Objects", "0:Drulling_Robot", '0:Degree', '0:degree2'])
    # degree3 = await root.get_child(["0:Objects", "0:Drulling_Robot", '0:Degree', '0:degree3'])
    # degree4 = await root.get_child(["0:Objects", "0:Drulling_Robot", '0:Degree', '0:degree4'])
    # degree5 = await root.get_child(["0:Objects", "0:Drulling_Robot", '0:Degree', '0:degree5'])
    # degree6 = await root.get_child(["0:Objects", "0:Drulling_Robot", '0:Degree', '0:degree6'])
    # degree7 = await root.get_child(["0:Objects", "0:Riveting_Robot", '0:Degree_R', '0:degree7'])
    # degree8 = await root.get_child(["0:Objects", "0:Riveting_Robot", '0:Degree_R', '0:degree8'])
    # degree9 = await root.get_child(["0:Objects", "0:Riveting_Robot", '0:Degree_R', '0:degree9'])
    # degree10 = await root.get_child(["0:Objects", "0:Riveting_Robot", '0:Degree_R', '0:degree10'])
    # degree11 = await root.get_child(["0:Objects", "0:Riveting_Robot", '0:Degree_R', '0:degree11'])
    # degree12 = await root.get_child(["0:Objects", "0:Riveting_Robot", '0:Degree_R', '0:degree12'])
    # x1 = await root.get_child(["0:Objects", "0:Drulling_Robot", '0:Joint', '0:x1'])
    # x2 = await root.get_child(["0:Objects", "0:Riveting_Robot", '0:Joint_R', '0:x2'])
    # y1 = await root.get_child(["0:Objects", "0:Drulling_Robot", '0:Joint', '0:y1'])
    # y2 = await root.get_child(["0:Objects", "0:Riveting_Robot", '0:Joint_R', '0:y2'])
    # z1 = await root.get_child(["0:Objects", "0:Drulling_Robot", '0:Joint', '0:z1'])
    # z2 = await root.get_child(["0:Objects", "0:Riveting_Robot", '0:Joint_R', '0:z2'])
    # a1 = await root.get_child(["0:Objects", "0:Drulling_Robot", '0:Joint', '0:a1'])
    # a2 = await root.get_child(["0:Objects", "0:Riveting_Robot", '0:Joint_R', '0:a2'])
    # b1 = await root.get_child(["0:Objects", "0:Drulling_Robot", '0:Joint', '0:b1'])
    # b2 = await root.get_child(["0:Objects", "0:Riveting_Robot", '0:Joint_R', '0:b2'])
    # c1 = await root.get_child(["0:Objects", "0:Drulling_Robot", '0:Joint', '0:c1'])
    # c2 = await root.get_child(["0:Objects", "0:Riveting_Robot", '0:Joint_R', '0:c2'])
    # normal1 = await root.get_child(["0:Objects", "0:Normals",'0:normal1'])
    # normal2 = await root.get_child(["0:Objects", "0:Normals",'0:normal2'])
    # normal3 = await root.get_child(["0:Objects", "0:Normals",'0:normal3'])

    # data=[actuator1,actuator2,actuator3,actuator4,degree1,degree2,degree3,degree4,
    #       degree5,degree6,degree7,degree8,degree9,degree10,degree11,degree12,x1,x2,
    #       y1,y2,z1,z2,a1,a2,b1,b2,c1,c2,normal1,normal2,normal3]

         # print(f'{bo}')
    # aa=await server.get_objects_node().get_child(
    #     ["0:Objects", "0:Server"]).nodeid
    # print(aa)
    # myobject2_type_nodeid = server.get_root_node().get_child(
    #     ["0:Types", "0:ObjectTypes", "0:BaseObjectType", "%d:StateType" % idx]).nodeid
    # myobject3_type_nodeid = server.get_node(ua.ObjectIds.BaseObjectType).get_child(
    #     ["%d:MyCustomObjectType" % idx]).nodeid
    #
    # # Node objects have methods to read and write node attributes as well as browse or populate address space
    # print("Children of root are: %r", await objects.get_children())

    # objects = server.get_objects_node()
    # aa = objects.get_child([f"{idx}:sss"])
    # aa.write_value(True)
    # print(aa)

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
