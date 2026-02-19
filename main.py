import os
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
Bootstrap(app)

# Load configuration from environment variables
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template("home.html")

# Register blueprints
from blue_prints.LOGIN.login import login_
from blue_prints.SETTINGS.settings import settings_
from blue_prints.SIEMENS.siemens import siemens_
from blue_prints.ROCKWELL.rockwell import rockwell_
from blue_prints.BECKOFF.beckoff import beckoff_
from blue_prints.KUKA.kuka import kuka_
from blue_prints.OPCUA.opcua import opcua_
from blue_prints.INFLUXDB.influxdb import influxdb_

app.register_blueprint(login_)
app.register_blueprint(settings_)
app.register_blueprint(siemens_)
app.register_blueprint(rockwell_)
app.register_blueprint(beckoff_)
app.register_blueprint(kuka_)
app.register_blueprint(opcua_)
app.register_blueprint(influxdb_)


################### app 主程序 （测试用） 部署版本采用nginx托管 ##########################
if __name__ == '__main__':
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 4000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host=host, debug=debug, port=port, threaded=True)