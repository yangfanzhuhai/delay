import random
import pickle
import os.path


def load_object(filename, default):
    if os.path.isfile(filename):
        return pickle.load(open(filename, "rb"))
    else:
        return default


def getRandomURL():
    url = ('http://delay.doc.ic.ac.uk:5000/'
           'predictions/?day={}&hour={}&run={}'
           '&route={}&naptan_atco={}')
    day1, hour1 = random.choice(day), random.choice(hour)
    try:
        run1, routes1 = random.choice(run), random.choice(routes)
        naptan_atco1 = random.choice(naptan_atco[(routes1, run1)])
    except KeyError:
        run1, routes1 = random.choice(run), random.choice(routes)
        naptan_atco1 = random.choice(naptan_atco[(routes1, run1)])
    return url.format(day1, hour1, run1, routes1, naptan_atco1)

run = [1, 2]
day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
       'Friday', 'Saturday', 'Sunday']
hour = list(range(24))

routes = load_object('routes.p', [])
naptan_atco = load_object('naptan_atco.p', {})

for i in range(1000):
    print(getRandomURL())
