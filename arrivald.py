import requests
from requests.auth import HTTPDigestAuth
import json
import pymysql
import sys
from datetime import datetime

# url = ('http://countdown.api.tfl.gov.uk/interfaces/ura/instant_V1'
url = ('http://countdown.api.tfl.gov.uk/interfaces/ura/stream_V1'
       '?ReturnList=StopID,LineName,VehicleID,TripID,EstimatedTime,ExpireTime')

r = requests.get(
    url,
    auth=HTTPDigestAuth('LiveBus95085', 'rU9HUx4ZEm'),
    # auth=('LiveBus95085', 'rU9HUx4ZEm'),
    stream=True,
)
print("Status Code:", r.status_code)

if r.status_code != requests.codes.ok:
    print("Received a bad status code from the server -- aborting")
    print(r.text)
    sys.exit()

conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='delay',
    passwd='CcwLCw3Kcs9Py33T',
    # user='root',
    # passwd='dta255dta',
    db='delay',
)
cur = conn.cursor()

sql_insert = ("INSERT INTO arrivals "
              "(stop_code_lbsl, route, vehicle_id, trip_id, "
              "arrival_time, expire_time, arrival_date) "
              "VALUES (%s, %s, %s, %s, %s, %s, DATE(%s)) "
              "ON DUPLICATE KEY UPDATE "
              "arrival_time=VALUES(arrival_time),"
              "expire_time=VALUES(expire_time)")

for line in r.iter_lines():
    if not line:
        continue
    # print(line)
    line = json.loads(line.decode('utf-8-sig'))
    if line[0] != 1:
        continue
    # print(line)
    line = line[1:]
    for i in [4, 5]:
        line[i] = int(line[i] / 1000)
        line[i] = datetime.fromtimestamp(line[i])
    line.append(line[5])
    # print(line)
    cur.execute(sql_insert, line)
    conn.commit()
conn.close()