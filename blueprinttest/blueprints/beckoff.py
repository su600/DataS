from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, send_file,Blueprint
from flask_bootstrap import Bootstrap

import random, datetime
from functools import wraps
import time
import functools
import os
from werkzeug.utils import secure_filename
import csv
import pandas as pd
import numpy as np
from struct import pack, unpack_from  # Pylogix 结构体解析
from blueprints.login import is_login

beckoff_ = Blueprint("beckoff_",__name__)

'''
倍福库文件 pyads
'''
#todo

########################### 倍福 ################################
@beckoff_.route("/beckoff",methods=["POST","GET"])
@is_login
def beckoff():
    # return render_template("b.html")
    # if request.method=='POST':
    #     aa=request.files.get("ss")
    return render_template("beckoff.html")