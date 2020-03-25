# opcua-influxdb-grafana-dummy
This is a repo for testing OPC UA, InfluxDB and Grafana.

The goal is to have dummy OPC UA server running on my local machine which pushes data to a cloud environment where the data is saved into InfluxDB and displayed using grafana.

## Files
* `server.py` has a dummy temperature and pressure sensor which is exposed with OPC UA.
* `client.py` has a reads the open OPC UA messages.
