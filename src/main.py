import os
from stats import Stats
from time import sleep

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

def read_secret_or_env(env:str):
    value=None
    if os.path.isfile(str(os.getenv(env+"_FILE"))):
        with open(os.getenv(env+"_FILE")) as secret:
            value = secret.read().rstrip('\n')
    else:
        value=os.getenv(env)
    return value;

influx_url = os.getenv('OMNI_INFLUX_URL')
influx_token = read_secret_or_env('OMNI_INFLUX_TOKEN')
influx_bucket = os.getenv('OMNI_INFLUX_BUCKET')
influx_org = os.getenv('OMNI_INFLUX_ORG')

client = InfluxDBClient(url=influx_url, token=influx_token)
write_api = client.write_api(write_options=SYNCHRONOUS)
data_rate = int(os.getenv('OMNI_DATA_RATE_SECONDS', 5))
stats = Stats()

max_tries=int(os.getenv('OMNI_MAX_ERRORS', default=5))
current_tries=0;

while True:
    print('Sending data...')
    data = stats.get_all(influx_format=True)
    try:
        write_api.write(influx_bucket, influx_org, data)
    except Exception as e:
        print("ERROR:", e);
        print()
        current_tries += 1
        if current_tries >= max_tries and max_tries != -1:
            exit(1)
    sleep(data_rate)
