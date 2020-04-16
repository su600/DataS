#1创建一个蓝图对象
from flask import Blueprint,url_for
ss = Blueprint("ss",__name__)
from blueprinttest.view22 import ss2
#2注册路由
#@app.route('/edit')改为
@ss.route('/edit')
def edit():
    url_for(ss2)
    return 'edit'
