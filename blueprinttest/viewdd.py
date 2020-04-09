#1创建一个蓝图对象
from flask import Blueprint
ss = Blueprint("ss",__name__)

#2注册路由
#@app.route('/edit')改为
@ss.route('/edit')
def edit():
    return 'edit'

@ss.route('/edit2')
def edit2():
    return 'edit2222222'