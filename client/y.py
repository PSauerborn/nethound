from uuid import UUID
from datetime import datetime, timedelta

from src.services.nethound import stream_timeseries


start = datetime.utcnow() - timedelta(hours=120)
network_id = UUID('6609e9e8-c20a-4db0-95de-5ce6b17cce41')


for p in stream_timeseries(network_id, start, datetime.utcnow()):
    print(p)