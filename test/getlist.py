from flask import Flask,render_template,request,redirect, url_for, flash, session, send_from_directory,send_file
from flask_bootstrap import Bootstrap
import random,datetime
from functools import wraps
import time
import functools
import os
from werkzeug.utils import secure_filename
import csv
import pandas as pd
import numpy as np

app = Flask(__name__)
Bootstrap(app)

## 设置密钥可以有效防止跨站请求伪造的攻击
app.config['SECRET_KEY'] = 'myproject'
app.secret_key = 'myproject'

@app.route("/",methods=["POST","GET"])
def geta():
    if request.method == "POST":
        flash("run", "run")
        # 该页面的表单信息，只要submit都传到这里
        forminfo = request.form.get('list')  # 获取不到value?？？？？？？？？？？？？
        print(forminfo)
    return render_template("a.html")

app.run()

