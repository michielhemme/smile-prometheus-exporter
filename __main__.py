from concurrent.futures import process
from multiprocessing.connection import wait
from prometheus_client import start_http_server, Gauge
from haanna import haanna
import time
import argparse

parser = argparse.ArgumentParser()

# -id SMILE_ID -ip SMILE_IP
parser.add_argument("-i", "--id", help="Smile identification code")
parser.add_argument("-I", "--ip",
                    help="Internet Address of the Smile device")
parser.add_argument("-p", "--port", help="Port to listen on (Default: 9101")
parser.add_argument("-a", "--address",
                    help="Address to listen on (Default: 0.0.0.0)")

args = parser.parse_args()

smile_id = args.id
smile_ip = args.ip
exporter_address = args.address or "0.0.0.0"
exporter_port = int(args.port) or 9101

API = haanna.Haanna("smile", smile_id, smile_ip, 80, False)

ROOM_TEMP = Gauge("smile_room_temp", "Current temperature of the room")
OUTDOOR_TEMP = Gauge("smile_outdoor_temp", "Current outdoor temperature")
SCHEDULED_TEMP = Gauge("smile_scheduled_temp", "Get the target temperature")


def set_metrics():
    _domain_objects = API.get_domain_objects()
    ROOM_TEMP.set(
        API.get_current_temperature(_domain_objects))
    OUTDOOR_TEMP.set(
        API.get_outdoor_temperature(_domain_objects))
    SCHEDULED_TEMP.set(
        API.get_target_temperature(_domain_objects))


if __name__ == "__main__":
    start_http_server(exporter_port, exporter_address)
    while True:
        set_metrics()
        time.sleep(30)
