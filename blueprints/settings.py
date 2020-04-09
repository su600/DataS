from flask import Flask,render_template,request,redirect, url_for, flash, session, send_from_directory,send_file
# from flask_bootstrap import Bootstrap
# import random,datetime
# from functools import wraps
# import time
# import functools
# import os
# from werkzeug.utils import secure_filename
# import csv
# import pandas as pd
# import numpy as np
# from struct import pack, unpack_from # Pylogix 结构体解析

from flask import Blueprint
from blueprints.login import is_login

settings_ = Blueprint("settings_",__name__)

@settings_.route("/setting")
@is_login
def setting():
    return render_template("setting.html")



