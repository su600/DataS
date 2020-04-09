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
from struct import pack, unpack_from # Pylogix 结构体解析

from flask import Blueprint
from blueprints.login import is_login

influxdb_ = Blueprint("influxdb_",__name__)

'''
influxDB 库文件
'''
from influxdb_client import InfluxDBClient,Point
# from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import random
import time

######################## InfluxDB 共用函数 #############################
@influxdb_.route("/influxDB",methods=("POST","GET"))
@is_login
def influxDB(influxdbip,token,measurement,cycle):
    print("influxDB写入")
    a=1
    bucket = "test"
    token="HTvG6oIApfABybjjYd_6Jehf8AEWkLStYw0qftanx9ijF05-UsLZ9pVqI604PwuRlhv8IkuIZshYaqVFTC0DXA=="
    client = InfluxDBClient(url=influxdbip,token=token,org="su")
    write_api = client.write_api(write_options=SYNCHRONOUS)
    # query_api = client.query_api()
    cycle=(int(cycle)/1000) #单位ms
    # cycle=(cycle)
    flash("开始写入influxDB","influx")
    while 1:
        try:
            ss=1
            xx=2
            p = Point(measurement).tag("location", "108厂房").field("温度", ss)
            q = Point(measurement).tag("location", "beijing").field("2", xx)
            write_api.write(bucket=bucket, org="su", record=[p,q])
            # print("2222")
            time.sleep(cycle)
        except a==0:
            pass # Stop writing

        except Exception as e:
            print(e)
            break