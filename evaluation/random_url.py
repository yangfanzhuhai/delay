import random
import pickle
import os.path
import argparse
import time


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


def getURL(t, day1, hour1):
    run1, routes1, naptan_atco1 = getRandomParams()
    return url.format(t, day1, hour1, run1, routes1, naptan_atco1)


def getRandomURL(t):
    day1, hour1 = random.choice(day), random.choice(hour)
    return getURL(t, day1, hour1)


def getCurrentURL(t):
    day1, hour1 = time.strftime("%A"), time.strftime("%H")
    return getURL(t, day1, hour1)


def getCurrentURLs():
    day1, hour1 = time.strftime("%A"), time.strftime("%H")
    run1, routes1, naptan_atco1 = getRandomParams()

    params = {'day': day1, 'hour': hour1, 'run': run1,
              'route': routes1, 'naptan_atco': naptan_atco1}

    return (url.format(url_types['pre'], day1, hour1,
                       run1, routes1, naptan_atco1),
            url.format(url_types['tfl'], day1, hour1,
                       run1, routes1, naptan_atco1),
            params)


url = ('http://delay.doc.ic.ac.uk:5000/'
       '{}/?day={}&hour={}&run={}'
       '&route={}&naptan_atco={}')

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
        print(getCurrentURL(url_types[args.url_type]))
