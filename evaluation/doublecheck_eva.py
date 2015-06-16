import pickle
import datetime


def printTime(ts):
    return datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')


record = pickle.load(open("evaluate_api.p", "rb"))
for k, v in record.items():
    print(k)
    print(v['next_vehicle'])
    for i, s in enumerate(v['stops']):
        record_time = float(v['record_time'])
        his = record_time + float(v['historical'][i])
        cur = record_time + float(v['current'][i])
        ref = record_time + float(v['reference'][i])
        his = printTime(his)
        cur = printTime(cur)
        ref = printTime(ref)
        print (s, his, cur, ref)
