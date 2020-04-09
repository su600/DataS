from blueprints.influxdb import *
from blueprints.login import is_login

opcua_ = Blueprint("opcua_",__name__)


'''
opcua库文件 本路由开发中 
'''
import opcua

######################## OPC UA Client 用于写入InfluxDB #################################### ToDo
@opcua_.route("/opcua")
@is_login
def opcua():
    # return render_template("b.html")
    return render_template("opcua.html")

######################## OPC UA Server 用于转换为OPC UA格式数据
# basic server仅支持UA expert Prosys还不支持 ########################
@opcua_.route("/opcuaserver")
@is_login
def opcuaserver():
    # return render_template("b.html")
    return render_template("opcua.html")