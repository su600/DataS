import os
import time
from flask import Blueprint, flash
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from blue_prints.LOGIN.login import is_login
from blue_prints.ROCKWELL.rockwell import rockwellread

influxdb_ = Blueprint("influxdb_", __name__)

######################## InfluxDB 共用函数 #############################
@influxdb_.route("/influxDB", methods=("POST", "GET"))
@is_login
def influxDB(influxdbip, token, measurement, cycle):
    print("influxDB写入")
    # Load configuration from environment variables
    bucket = os.environ.get('INFLUXDB_BUCKET', 'data')
    org = os.environ.get('INFLUXDB_ORG', 'su')
    
    # Use token from parameter or environment variable
    if not token:
        token = os.environ.get('INFLUXDB_TOKEN', '')
    
    if not token:
        flash("InfluxDB token not configured", "error")
        return
    
    client = InfluxDBClient(url=influxdbip, token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    
    # Cycle in seconds
    cycle = int(cycle)
    
    flash("开始写入influxDB", "influx")
    previous_data = {}
    
    while True:
        try:
            data = rockwellread()[1]
            
            # Only write points that have changed values
            points_to_write = []
            for field_name, field_value in data.items():
                # Check if value changed or is new
                if field_name not in previous_data or previous_data[field_name] != field_value:
                    point = Point(measurement).tag("location", "#108 Plant").field(field_name, field_value)
                    points_to_write.append(point)
            
            if points_to_write:
                write_api.write(bucket=bucket, org=org, record=points_to_write)
            
            # Update previous data
            previous_data = data.copy()
            time.sleep(cycle)
        except Exception as e:
            print(f"influxDB写入出错了: {e}")
            break