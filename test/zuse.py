###### Flask1.0以上 支持非阻塞
from flask import Flask
import time

app = Flask(__name__)
app.config.update(DEBUG=True)


@app.route('/first')
def first_request():

    print('开始执行 first')
    time.sleep(10)
    print('结束执行 first')

    return 'Hello First!'


@app.route('/second')
def second_request():

    print('执行second')
    return 'Hello Second!'


if __name__ == '__main__':
    app.run()
