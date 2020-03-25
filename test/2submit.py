from flask import Flask,render_template,request,redirect, url_for, flash, session
from flask_bootstrap import Bootstrap
import random,datetime
from functools import wraps
import time
import functools
import os


from flask import *
from wtforms import *
# from wtforms.validators import Required
#

class Form1():
    name = StringField('name')
    submit1 = SubmitField('submit')


class Form2():
    name = StringField('name')
    submit2 = SubmitField('submit')



form1 = Form1()
form2 = Form2()


if form1.submit1.data and form1.validate_on_submit():  # 注意顺序
    pass
if form2.submit2.data and form2.validate_on_submit():  # 注意顺序
    pass

app=Flask(__name__)

@app.route("/2submit",methods=["POST","GET"])
def test():

    if request.method=="POST":
        aa=request.form.to_dict()
        print(aa)
    return render_template("2submit.html")

# @app.route("/2submit",methods=["POST","GET"])
# def test2():
#     if request.method=="POST":
#         aa=request.form.to_dict()
#         print(aa)
#     return render_template("2submit.html")

app.run()