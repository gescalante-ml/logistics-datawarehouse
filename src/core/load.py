import csv

from . import dimension
from ..services import sql


def start(headers, data):
    """Batches processes the data, based on the header"""
    runs = []

    # Data structutures to hold dimensions of the fact
    cities = set()
    shippers = set()
    carriers = {}
    loads = {}
    on_times = {}
    trackings = {}

    for record in data:
        truck_run = dict(zip(headers, record))
        truck_run = transform(truck_run)

        # Creates id for avoid duplicates before searching for the data that is already on the db
        carrier_id = ''.join([str(value) for key, value in truck_run['carrier_key'].items()])
        load_id = ''.join([str(value) for key, value in truck_run['load_key'].items()])
        on_time_id = ''.join([str(value) for key, value in truck_run['on_time_key'].items()])
        tracking_id = ''.join([str(value) for key, value in truck_run['tracking_key'].items()])

        # Updates the data structures
        if truck_run['origin'] not in cities:
            cities.add(truck_run['origin'])
        if truck_run['destination'] not in cities:
            cities.add(truck_run['destination'])
        if truck_run['shipper_name'] not in shippers:
            shippers.add(truck_run['shipper_name'])
        if carrier_id not in carriers:
            carriers[carrier_id] = truck_run['carrier_key']
        if load_id not in loads:
            loads[load_id] = truck_run['load_key']
        if on_time_id not in on_times:
            on_times[on_time_id] = truck_run['on_time_key']
        if tracking_id not in trackings:
            trackings[tracking_id] = truck_run['tracking_key']
        runs.append(truck_run)

    # Searches the ids for the dimensions, and create if don't exist
    carriers = sql.get_carriers_ids(carriers, insert_new=True)
    on_times = sql.get_on_time_ids(on_times, insert_new=True)
    loads = sql.get_load_ids(loads, insert_new=True)
    trackings = sql.get_tracking_ids(trackings, insert_new=True)
    cities = sql.get_city_ids(cities, insert_new=True)
    shippers = sql.get_shipper_ids(shippers, insert_new=True)

    # Changes raw data to dimension ids
    for truck_run in runs:
        carrier_id = ''.join([str(value) for key, value in truck_run['carrier_key'].items() if key != 'carrier_key'])
        load_id = ''.join([str(value) for key, value in truck_run['load_key'].items() if key != 'load_key'])
        on_time_id = ''.join([str(value) for key, value in truck_run['on_time_key'].items() if key != 'on_time_key'])
        tracking_id = ''.join([str(value) for key, value in truck_run['tracking_key'].items() if key != 'tracking_key'])

        shipper = truck_run['shipper_name']
        destination = truck_run['destination']
        origin = truck_run['origin']

        if carrier_id in carriers:
            truck_run['carrier_key'] = carriers[carrier_id]['carrier_key']

        if load_id in loads:
            truck_run['load_key'] = loads[load_id]['load_key']

        if on_time_id in on_times:
            truck_run['on_time_key'] = on_times[on_time_id]['on_time_key']

        if tracking_id in trackings:
            truck_run['tracking_key'] = trackings[tracking_id]['tracking_key']

        if origin in cities:
            truck_run['origin_location_key'] = cities[origin]['location_key']
            del truck_run['origin']

        if destination in cities:
            truck_run['destination_location_key'] = cities[destination]['location_key']
            del truck_run['destination']

        if shipper in shippers:
            truck_run['shipper_key'] = shippers[shipper]['shipper_key']
            del truck_run['shipper_name']

    # Insert the facts to the data warehouse
    sql.insert_facts(runs)


def transform(truck_run):
    """Transform raw data in dimensions"""
    truck_run = dimension.equipment_type_dimension(truck_run)
    truck_run = dimension.sourcing_channel_dimension(truck_run)
    truck_run = dimension.load_dimension(truck_run)
    truck_run = dimension.location_dimension(truck_run)
    truck_run = dimension.carrier_dimension(truck_run)
    truck_run = dimension.on_time_dimension(truck_run)
    truck_run = dimension.tracking_dimension(truck_run)
    truck_run = dimension.time_dimensions(truck_run)

    truck_run = fact(truck_run)

    return truck_run


def fact(truck_run):
    """Loads numeric metrics of the fields"""
    truck_run['book_price'] = float(truck_run['book_price'])
    truck_run['source_price'] = float(truck_run['source_price'])
    truck_run['mileage'] = float(truck_run['mileage'])
    truck_run['profit_and_loss'] = float(truck_run['pnl'])

    del truck_run['pnl']

    return truck_run
