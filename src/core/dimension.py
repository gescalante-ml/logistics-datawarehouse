from ..data import equipment_type, sourcing_channel


def equipment_type_dimension(truck_run):
    truck_run['equipment_type_key'] = equipment_type.get(truck_run['equipment_type'], 1)
    del truck_run['equipment_type']
    return truck_run


def sourcing_channel_dimension(truck_run):
    truck_run['sourcing_channel_key'] = equipment_type.get(truck_run['sourcing_channel'], 1)
    del truck_run['sourcing_channel']
    return truck_run


def load_dimension(truck_run):
    indicators = ['contracted_load', 'load_was_cancelled', 'load_booked_autonomously', 'load_sourced_autonomously']
    load_dimension_ = {}
    load_dimension_['contracted_indicator'] = 'Contracted' if truck_run['contracted_load'] == 'TRUE' else 'Not Contracted'
    load_dimension_['cancelled_indicator'] = 'Cancelled' if truck_run['load_was_cancelled'] == 'TRUE' else 'Not Cancelled'
    load_dimension_['booked_indicator'] = 'Booked Autonomously' if truck_run['load_booked_autonomously'] == 'TRUE' else 'Not Booked Autonomously'
    load_dimension_['sourced_indicator'] = 'Sourced Autonomously' if truck_run['load_sourced_autonomously'] == 'TRUE' else 'Not Sourced Autonomously'

    truck_run['load_dimension_key'] = load_dimension_
    for indicator in indicators:
        del truck_run[indicator]

    return truck_run


def on_time_dimension(truck_run):
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


def location_dimension(truck_run):
    origin, destination = truck_run['lane'].split(' -> ')

    truck_run['origin'] = origin
    truck_run['destination'] = destination
    del truck_run['lane']

    return truck_run


def carrier_dimension(truck_run):

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
    truck_run['carrier'] = carrier

    return truck_run


def tracking_dimension(truck_run):
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

