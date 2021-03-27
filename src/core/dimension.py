from ..data import equipment_type, sourcing_channel
from ..utils import load_datestring


def equipment_type_dimension(truck_run):
    """Transforms raw equipment type in a dimensional key"""
    truck_run['equipment_type_key'] = equipment_type.get(truck_run['equipment_type'], 1)
    del truck_run['equipment_type']
    return truck_run


def sourcing_channel_dimension(truck_run):
    """Transforms raw sourcing channel type in a dimensional key"""
    truck_run['sourcing_channel_key'] = sourcing_channel.get(truck_run['sourcing_channel'], 1)
    del truck_run['sourcing_channel']
    return truck_run


def load_dimension(truck_run):
    """Transforms raw load informations in a junk dimensional model to insert as needed"""
    indicators = ['contracted_load', 'load_was_cancelled', 'load_booked_autonomously', 'load_sourced_autonomously']
    load_dimension_ = {}
    load_dimension_['contracted_indicator'] = 'Contracted' if truck_run['contracted_load'] == 'TRUE' else 'Not Contracted'
    load_dimension_['cancelled_indicator'] = 'Cancelled' if truck_run['load_was_cancelled'] == 'TRUE' else 'Not Cancelled'
    load_dimension_['booked_indicator'] = 'Booked Autonomously' if truck_run['load_booked_autonomously'] == 'TRUE' else 'Not Booked Autonomously'
    load_dimension_['sourced_indicator'] = 'Sourced Autonomously' if truck_run['load_sourced_autonomously'] == 'TRUE' else 'Not Sourced Autonomously'

    truck_run['load_key'] = load_dimension_
    for indicator in indicators:
        del truck_run[indicator]

    return truck_run


def on_time_dimension(truck_run):
    """Transforms raw carrier_on_time informations in a junk dimensional model to insert as needed"""
    indicators = ['carrier_on_time_to_pickup', 'carrier_on_time_to_delivery', 'carrier_on_time_overall']
    on_time = {}
    on_time['pickup_indicator'] = (
        'Carrier On Time To Pickup' if truck_run['carrier_on_time_to_pickup'] == 'TRUE'
        else 'Carrier Not On Time To Pickup'
    )
    on_time['delivery_indicator'] = (
        'Carrier On Time To Delivery' if truck_run['carrier_on_time_to_delivery'] == 'TRUE'
        else 'Carrier Not On Time To Delivery'
    )
    on_time['overall_indicator'] = (
        'Carrier On Time Overall' if truck_run['carrier_on_time_overall'] == 'TRUE'
        else 'Carrier Not On Time Overall'
    )

    truck_run['on_time_key'] = on_time
    for indicator in indicators:
        del truck_run[indicator]

    return truck_run


def lane_dimension(truck_run):
    """Transforms raw lane information in lane dimension"""
    lane = {}
    origin, destination = truck_run['lane'].split(' -> ')
    origin = origin.split(',')
    destination = destination.split(',')
    lane['origin_city'], lane['origin_state'] = origin
    lane['origin_country'] = 'USA'
    lane['mileage'] = float(truck_run['mileage'])
    lane['destination_city'], lane['destination_state'] = destination
    lane['destination_country'] = 'USA'
    lane['city_pair'] = f"{lane['origin_city']}, {lane['origin_state']} -> {lane['destination_city']}, {lane['destination_state']}"

    truck_run['lane_key'] = lane

    raw_fields = ['lane', 'mileage']
    for field in raw_fields:
        del truck_run[field]

    return truck_run


def carrier_dimension(truck_run):
    """Transforms raw carrier information in carrier dimensional model"""
    carrier = {
        'carrier_name': truck_run['carrier_name'],
        'vip_indicator': 'VIP' if truck_run['vip_carrier'] == 'TRUE' else 'Not VIP',
        'carrier_rating': truck_run['carrier_rating'].replace('.0', '') if truck_run['carrier_rating'] != '' else None,
        'carrier_dropped': truck_run['carrier_dropped_us_count']
    }

    del truck_run['carrier_name']
    del truck_run['vip_carrier']
    del truck_run['carrier_rating']
    del truck_run['carrier_dropped_us_count']
    truck_run['carrier_key'] = carrier

    return truck_run


def tracking_dimension(truck_run):
    """Transforms raw tracking information in junk dimensional model to insert as needed"""
    indicators = ['has_mobile_app_tracking', 'has_macropoint_tracking', 'has_edi_tracking']
    tracking = {}
    tracking['mobile_app_indicator'] = (
        'Mobile App Tracked' if truck_run['has_mobile_app_tracking'] == 'TRUE'
        else 'Not Macro Point Tracked'
    )
    tracking['macro_point_indicator'] = (
        'Macro Point Tracked' if truck_run['has_macropoint_tracking'] == 'TRUE'
        else 'Not Macro Point Tracked'
    )
    tracking['edi_indicator'] = (
        'EDI Tracked' if truck_run['has_edi_tracking'] == 'TRUE'
        else 'Not EDI Tracked'
    )

    truck_run['tracking_key'] = tracking
    for indicator in indicators:
        del truck_run[indicator]

    return truck_run


def time_dimensions(truck_run):
    """Loads all time dimensions"""
    truck_run.update(load_datestring(truck_run['book_date'], 'book_'))
    truck_run.update(load_datestring(truck_run['quote_date'], 'quote_'))
    truck_run.update(load_datestring(truck_run['source_date'], 'source_'))

    truck_run.update(load_datestring(truck_run['delivery_appointment_time'], 'delivery_appointment_'))
    truck_run.update(load_datestring(truck_run['delivery_date'], 'delivery_'))

    truck_run.update(load_datestring(truck_run['pickup_appointment_time'], 'pickup_appointment_'))
    truck_run.update(load_datestring(truck_run['pickup_date'], 'pickup_'))

    return truck_run

