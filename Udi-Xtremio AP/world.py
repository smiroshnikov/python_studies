from csv import DictReader
from math import radians, cos, sin, asin, sqrt

ISRAEL_LAT, ISRAEL_LON = 31.5, 34.75


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km


with open('cow.csv') as f:
    reader = DictReader(f)
    for d in reader:
        print (d['name'], ":", int(haversine(ISRAEL_LAT, ISRAEL_LON, float(d['lat']), float(d['lon']))), "km")
