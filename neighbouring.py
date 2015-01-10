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


with open('generated/neighbouring.csv', 'w') as out:
    writer = csv.writer(out)
    writer.writerow(['route', 'start_stop_code_lbsl', 'end_stop_code_lbsl'])
    for entry in data.values():
        seq = sorted(entry.items(), key=lambda x: x[0])
        for current, nxt in zip(seq, seq[1:]):
            writer.writerow([current[1]['Route'],
                            current[1]['Stop_Code_LBSL'],
                            nxt[1]['Stop_Code_LBSL']])
