import requests
from requests.auth import HTTPDigestAuth
import json
import pymysql
import sys
from datetime import datetime

# recorded time after 2015-06-02 15:40:01

# url = ('http://countdown.api.tfl.gov.uk/interfaces/ura/instant_V1'
url = ('http://countdown.api.tfl.gov.uk/interfaces/ura/instant_V1?ReturnList=StopID,LineName,DirectionID,VehicleID,TripID,EstimatedTime,ExpireTime')

r = requests.get(
    url,
    # auth=HTTPDigestAuth('LiveBus95085', 'rU9HUx4ZEm'),
    auth=('LiveBus95085', 'rU9HUx4ZEm'),
    # stream=True,
)
print("Status Code:", r.status_code)

if r.status_code != requests.codes.ok:
    print("Received a bad status code from the server -- aborting")
    print(r.text)
    sys.exit()

conn = pymysql.connect(
    # host='localhost',
    host='delay.doc.ic.ac.uk',
    port=3306,
    user='delay',
    passwd='CcwLCw3Kcs9Py33T',
    # user='root',
    # passwd='dta255dta',
    db='delay',
)
cur = conn.cursor()

sql_insert_full = ("INSERT INTO delay_arrivals_full "
                   "(stop_code_lbsl, route, run, vehicle_id, trip_id, "
                   "arrival_time, expire_time, arrival_date, recorded_time) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, DATE(%s), %s) ")

for line in r.iter_lines():
    if not line:
        continue
    line = json.loads(line.decode('utf-8-sig'))
    if line[0] != 1:
        continue
    line = line[1:]
    for i in [5, 6]:
        line[i] = int(line[i] / 1000)
    line[5] = datetime.fromtimestamp(line[5])
    if line[6] == 0:
        line[6] = None
    else:
        line[6] = datetime.fromtimestamp(line[6])
    line.append(line[5])
    line.append(datetime.now())
    # print(line[0:5], line[5].strftime("%H:%M:%S"), line[6])
    cur.execute(sql_insert_full, line)

conn.commit()
conn.close()
