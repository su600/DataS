from blueprints.influxdb import *
from blueprints.login import is_login

opcua_ = Blueprint("opcua_",__name__)

# from main import *
from blueprints.forms import ServerCreateForm
'''
opcua库文件 本路由开发中 
'''
# from flask_wtf.csrf import CSRFProtect
# csrf = CSRFProtect()

######################## OPC UA Client 用于写入InfluxDB #################################### ToDo
@opcua_.route("/opcua")
@is_login
def opcua():
    # return render_template("b.html")
    form = ServerCreateForm()
    return render_template("opcua.html",form=form)

######################## OPC UA Server 用于转换为OPC UA格式数据
# basic server仅支持UA expert Prosys还不支持 ########################
@opcua_.route("/opcuaserver")
@is_login
def opcuaserver():
    # return render_template("b.html")
    return render_template("opcua.html")


@opcua_.route("/o",methods=['GET','POST'])
@is_login
def create_server():
    print('create-server')
    # return render_template("b.html")
    return redirect('opcua')