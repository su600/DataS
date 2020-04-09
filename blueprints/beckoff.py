from blueprints.influxdb import *
from blueprints.login import is_login

beckoff_ = Blueprint("beckoff_",__name__)

'''
倍福库文件 pyads
'''
#todo

########################### 倍福 ################################
@beckoff_.route("/beckoff",methods=["POST","GET"])
@is_login
def beckoff():
    # return render_template("b.html")
    # if request.method=='POST':
    #     aa=request.files.get("ss")
    return render_template("beckoff.html")