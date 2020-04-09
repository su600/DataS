from flask import Flask

app=Flask(__name__)

@app.route('/')
def index():
    return 'index'

#3.在应用对象上注册这个蓝图对象
from blueprinttest.viewdd import *
app.register_blueprint(ss)

if __name__=='__main__':
    app.run()