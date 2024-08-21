# https://github.com/ip2location/ip2location-iata-icao/blob/master/iata-icao.csv

import pdb
import pytz
import pandas as pd
from time import sleep
from datetime import datetime, time, timedelta

from opensky_api import OpenSkyApi, Waypoint, StateVector

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

def norm(d: datetime) -> int:
    return to_secs(to_utc(d))

def to_datetime(ts: int) -> datetime:
    return datetime.fromtimestamp(ts, pytz.utc))

dtime = datetime(2024,8,16, hour=18, minute=30) # 6pm
two_hr = dtime + timedelta(hours=2)

sod = min_timestamp(dtime)
eod = max_timestamp(dtime)
s = norm(dtime)
e = norm(two_hr)

api = OpenSkyApi()
flights = api.get_departures_by_airport(
    "KIAH", # Hobby (none, use IAH) 
    norm(sod),
    norm(eod)
)
sod = min_timestamp(dtime)

to_sd = [
    f for f in flights
    if f.estArrivalAirport=="KSAN"
]

airports = [f.estArrivalAirport for f in flights] 
# print(f"{airports=}")
# print(f"{to_sd=}")

icao24 = to_sd[-1].icao24
# print(to_sd[-1])
track = api.get_track_by_aircraft(
    icao24, t=to_sd[-1].firstSeen
)

points = [
    Waypoint(p).__dict__
    for p in track.path
]

df = pd.DataFrame(points)
print(df)
N = 15
df = (
    df
    .assign(timestamp=df["time"].apply(
        lambda x: 
        datetime.fromtimestamp(x, pytz.utc))
    )
    .set_index("timestamp")
    #.resample("15min")
    #.first()
    .iloc[::N, :]
)

print(df)
times = df["time"].tolist()
states = []
for t in times:
    s = api.get_states(t,icao24=icao24)
    states.append(s)
    sleep(2)

pdb.set_trace()

print(f"{states=}")

blips = pd.DataFrame([
    s.states[0].__dict__ for s in states
    if s
    ]).assign(
        time_position=lambda x: 
        x["time_position"].apply(to_datetime
    )

blips[[
    "time_position",
    "velocity",
    "geo_altitude"
]] 

pdb.set_trace()
print(blips)

# print(f"{type(track.path[0][0])=}")



# states = api.get_states(
#    to_sd[-1].firstSeen,
#    icao24=icoa24
#)


print(f"{states=}")

