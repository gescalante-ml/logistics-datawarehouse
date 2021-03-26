import csv

from . import dimension


def start(headers, data):

    for record in data:
        truck_run = dict(zip(headers, record))
        truck_run = transform(truck_run)
        cities = set()
        if truck_run['origin'] not in cities:
            cities.add(truck_run['origin'])
        if truck_run['destination'] not in cities:
            cities.add(truck_run['destination'])

    from pprint import pprint
    pprint(truck_run)


def transform(truck_run):
    truck_run = dimension.equipment_type_dimension(truck_run)
    truck_run = dimension.sourcing_channel_dimension(truck_run)
    truck_run = dimension.load_dimension(truck_run)
    truck_run = dimension.location_dimension(truck_run)
    truck_run = dimension.carrier_dimension(truck_run)
    truck_run = dimension.on_time_dimension(truck_run)
    truck_run = dimension.tracking_dimension(truck_run)

    return truck_run



