import csv
import pickle


routes = []

with open('bus_routes.csv', 'r', encoding='utf-8-sig') as file:
    reader = csv.reader(file)
    for row in reader:
        # print(row)
        routes.extend(row)
print(routes)
pickle.dump(routes, open("routes.p", "wb"))


data = {}

with open('../data/bus-sequences.csv', 'r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    for row in reader:
        try:
            run = int(row['Run'])
            current_key = (row['Route'], run)
            if current_key in data:
                current = data[current_key]
                current.append(row['Naptan_Atco'])
                data[current_key] = current
            else:
                data[current_key] = [row['Naptan_Atco']]
        except TypeError:
            print('Invalid sequence number: row not inserted', row)
# print(data)
pickle.dump(data, open("naptan_atco.p", "wb"))
