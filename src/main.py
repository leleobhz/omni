import os
from stats import Stats
from time import sleep

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from get_docker_secret import get_docker_secret

influx_url = os.getenv('OMNI_INFLUX_URL')
influx_token = get_docker_secret('OMNI_INFLUX_TOKEN_FILE', getEnv=False)
if influx_token is None:
    influx_token = os.getenv('OMNI_INFLUX_TOKEN')
if influx_token is None:
    raise ValueError("Influx Token not set")

influx_bucket = os.getenv('OMNI_INFLUX_BUCKET')
influx_org = os.getenv('OMNI_INFLUX_ORG')

client = InfluxDBClient(url=influx_url, token=influx_token)
write_api = client.write_api(write_options=SYNCHRONOUS)
data_rate = int(os.getenv('OMNI_DATA_RATE_SECONDS', 5))
stats = Stats()

max_tries=5
current_tries=0;

while True:
    print('Sending data...')
    data = stats.get_all(influx_format=True)
    try:
        write_api.write(influx_bucket, influx_org, data)
    except Exception as e:
        print(e);
        current_tries += 1
        if current_tries >= max_tries:
            exit()
    sleep(data_rate)
