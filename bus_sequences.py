import csv
from collections import defaultdict


data = defaultdict(dict)

with open('data/bus-sequences.csv', 'r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    for row in reader:
        try:
            data[row['Route'], row['Run']][int(row['Sequence'])] = row
        except TypeError:
            print('Invalid sequence number: row not inserted', row)

with open('generated/bus_sequences_corrected.csv', 'w') as out:
    writer = csv.writer(out)
    writer.writerow(['route', 'run', 'sequence', 'stop_code_lbsl',
                     'bus_stop_code', 'naptan_atco', 'stop_name',
                     'location_easting', 'location_northing',
                     'heading', 'virtual_bus_stop'])

    for entry in data.values():
        seq = sorted(entry.items(), key=lambda x: x[0])
        for index, (key, stop) in enumerate(seq):
            stop['Sequence'] = index + 1
            writer.writerow([stop['Route'], stop['Run'], stop['Sequence'],
                             stop['Stop_Code_LBSL'], stop['Bus_Stop_Code'],
                             stop['Naptan_Atco'], stop['Stop_Name'],
                             stop['Location_Easting'],
                             stop['Location_Northing'],
                             stop['Heading'], stop['Virtual_Bus_Stop']])
