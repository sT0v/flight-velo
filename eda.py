# https://github.com/ip2location/ip2location-iata-icao/blob/master/iata-icao.csv

from datetime import datetime
from opensky_api import OpenSkyApi
from datetime import datetime, time, timedelta


start_of_day = datetime.combine(datetime.now(),time.min)

end_of_day = datetime.combine(datetime.now(), time.max)

two_hr = start_of_day + timedelta(hours=2)

t=int(two_hr.strftime("%s"))
s=int(start_of_day.strftime("%s"))
e=int(end_of_day.strftime("%s"))

api = OpenSkyApi()
f = api.get_flights_from_interval(s,t) # 2hrs
icoa24 = f[-1].icao24
