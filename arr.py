# https://github.com/ip2location/ip2location-iata-icao/blob/master/iata-icao.csv

import pytz
from datetime import datetime
from opensky_api import OpenSkyApi
from datetime import datetime, time, timedelta


def to_secs(d: datetime) -> int:
    return int(d.strftime("%s"))

def min_timestamp(d: datetime) -> datetime:
    return datetime.combine(d, time.min)

def max_timestamp(d: datetime) -> datetime:
    return datetime.combine(d, time.max)

def to_utc(d: datetime, tz: str = "US/Central") -> datetime:

    local = pytz.timezone(tz)
    naive = d
    local_dt = local.localize(
        naive, is_dst=None
    )
    utc_dt = local_dt.astimezone(pytz.utc)
    return utc_dt

dtime = datetime(2024,8,16, hour=18) # 6pm
two_hr = dtime + timedelta(hours=2)

s = to_secs(to_utc(dtime))
e = to_secs(to_utc(two_hr))

api = OpenSkyApi()
f = api.get_arrivals_by_airport(
        "KSAN", 
        s,e
        ) # 2hrs
icoa24 = f[-1].icao24

print(icoa24)

