#1创建一个蓝图对象
from flask import Blueprint,url_for
from blueprinttest.view22 import edit2

ss = Blueprint("ss",__name__)

#2注册路由
#@app.route('/edit')改为
@ss.route('/edit')
def edit():
    # url_for(ss2)
    edit2()
    return 'edit'

