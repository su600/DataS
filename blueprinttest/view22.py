#1创建一个蓝图对象
from flask import Blueprint
ss2 = Blueprint("ss2",__name__)

#2注册路由
#@app.route('/edit')改为
@ss2.route('/22')
def edit():
    return '22'