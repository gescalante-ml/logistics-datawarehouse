import csv

from src.core import load

if __name__ == '__main__':
    with open('logistics_data.csv', 'r') as f:
        rows = csv.reader(f, delimiter=',')
        headers = []
        batch = []
        for i, row in enumerate(rows):
            if i == 0:
                headers = row
                continue
            batch.append(row)
            if i > 500:
                break

    load.start(headers, batch)