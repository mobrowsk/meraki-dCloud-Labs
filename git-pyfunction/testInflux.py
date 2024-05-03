import json
import os
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv

load_dotenv()

# InfluxDB settings
INFLUXDB_URL = os.environ['influx_url']
INFLUXDB_TOKEN = os.environ['influx_token']
INFLUXDB_ORG = os.environ['influx_org']
INFLUXDB_BUCKET = os.environ['influx_bucket']

# Your JSON data
'''with open("devices.json", "r") as json_file:
    json_data = json.load(json_file)'''

class InfluxDB:
    def __init__(self):
        # Initialize InfluxDB client
        self.client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)


    def writeDevicestoDB(self, meraki_response):
        # Prepare and write data points
        for org_id, devices in meraki_response.items():
            for device in devices:
                point = (
                    Point("demo")
                    .tag("organizationId", device["organizationId"])
                    .tag("orgName", device["org_name"])
                    .tag("networkId", device["network"])
                    .tag("deviceType", device["productType"])
                    .tag("name", device["name"])
                    .field("name", device["name"])
                    .field("status", device["status"])
                    .field("name", device["name"])
                    .field("productType", device["productType"])
                    .field("networkId", device["network"]["id"])
                    .field("statusNumerical", device["status_numerical"])
                )
                # Write the point to the InfluxDB bucket
                self.write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
        # Close the client
        self.client.close()


