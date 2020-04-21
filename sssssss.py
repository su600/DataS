from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, send_file,Blueprint
from flask_bootstrap import Bootstrap
import random,datetime,time

app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = 'myproject'
app.secret_key = 'myproject'


@app.route("/")
def a():

    ttt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # except Exception as e:
    # print(e)
    # else:
    # flash(data, "value")
    # flash(ttt, "time")
    # flash(variable,"variable")
    # siemensdata = dict(zip(variable, data))
    siemensdata={"1":True,"2":False}
    print(siemensdata)
    # todo 返回值显示
    return render_template("siemens.html", siemensdata=siemensdata, ttt=ttt)

app.run()