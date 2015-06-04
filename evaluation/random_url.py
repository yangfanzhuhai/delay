import random
import pickle
import os.path
import argparse


def load_object(filename, default):
    if os.path.isfile(filename):
        return pickle.load(open(filename, "rb"))
    else:
        return default


def getRandomParams():
    try:
        run1, routes1 = random.choice(run), random.choice(routes)
        naptan_atco1 = random.choice(naptan_atco[(routes1, run1)])
    except KeyError:
        run1, routes1 = random.choice(run), random.choice(routes)
        naptan_atco1 = random.choice(naptan_atco[(routes1, run1)])
    return (run1, routes1, naptan_atco1)


def getRandomURL(t):
    url = ('http://delay.doc.ic.ac.uk:5000/'
           '{}/?day={}&hour={}&run={}'
           '&route={}&naptan_atco={}')
    day1, hour1 = random.choice(day), random.choice(hour)
    run1, routes1, naptan_atco1 = getRandomParams()
    return url.format(t, day1, hour1, run1, routes1, naptan_atco1)


run = [1, 2]
day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
       'Friday', 'Saturday', 'Sunday']
hour = list(range(24))

routes = load_object('routes.p', [])
naptan_atco = load_object('naptan_atco.p', {})

url_types = {'tfl': 'tfl_timetable', 'pre': 'predictions'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("url_type")
    parser.add_argument("number")
    args = parser.parse_args()
    for i in range(int(args.number)):
        print(getRandomURL(url_types[args.url_type]))
