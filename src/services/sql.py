import os
import mysql.connector

mydb = mysql.connector.connect(
    host=os.environ['DWH_HOST'],
    user=os.environ['DWH_USER'],
    password=os.environ['DWH_PASSWORD'],
    database=os.environ['DWH_DATABASE']
)

mycursor = mydb.cursor()


def get_carriers_ids(carriers, insert_new=False):
    columns = ['carrier_key', 'carrier_name', 'vip_indicator', 'carrier_rating', 'carrier_dropped']

    carriers_name = tuple([carriers[carrier]['carrier_name'] for carrier in carriers])
    query = f"""SELECT carrier_key, carrier_name, vip_indicator, carrier_rating, carrier_dropped FROM carrier_d WHERE
    carrier_name in {carriers_name}
    """
    mycursor.execute(query)
    rows = mycursor.fetchall()
    lines = []
    for row in rows:
        carrier = dict(zip(columns, row))

        carrier_id = ''.join([str(value) for key, value in carrier.items() if key != 'carrier_key'])

        if carrier_id in carriers:
            carriers[carrier_id]['carrier_key'] = carrier['carrier_key']

    if not insert_new:
        return carriers

    for key, carrier in carriers.items():
        if 'carrier_key' not in carrier:
            lines.append(tuple([value for k, value in carrier.items()]))

    insert_sql = f"INSERT INTO carrier_d(carrier_name, vip_indicator, carrier_rating, carrier_dropped) VALUES (%s, %s, %s, %s)"


    if len(lines) > 0:
        mycursor.executemany(insert_sql, lines)
        mydb.commit()
        print(mycursor.rowcount, "was inserted.")
    else:
        print('Nothing new')

    return get_carriers_ids(carriers)


def get_on_time_ids(on_times, insert_new=False):
    columns = [
        'on_time_key',
        'pickup_indicator',
        'delivery_indicator',
        'overall_indicator'
    ]

    query = f"""SELECT on_time_key, pickup_indicator, delivery_indicator, overall_indicator FROM on_time_d"""
    mycursor.execute(query)
    rows = mycursor.fetchall()
    lines = []
    for row in rows:
        on_time = dict(zip(columns, row))

        on_time_id = ''.join([str(value) for key, value in on_time.items() if key != 'on_time_key'])

        if on_time_id in on_times:
            on_times[on_time_id]['on_time_key'] = on_time['on_time_key']

    if not insert_new:
        return on_times

    for key, on_time in on_times.items():
        if 'on_time_key' not in on_time:
            lines.append(tuple([value for k, value in on_time.items()]))


    insert_sql = f"INSERT INTO on_time_d(pickup_indicator, delivery_indicator, overall_indicator) VALUES (%s, %s, %s)"

    if len(lines) > 0:
        mycursor.executemany(insert_sql, lines)
        mydb.commit()
        print(mycursor.rowcount, "was inserted.")
    else:
        print('Nothing new')

    return get_on_time_ids(on_times)


def get_load_ids(loads, insert_new=False):
    columns = [
        'load_key',
        'contracted_indicator',
        'cancelled_indicator',
        'booked_indicator',
        'sourced_indicator'
    ]

    query = f"""SELECT load_key, contracted_indicator, cancelled_indicator, booked_indicator, sourced_indicator FROM load_d"""
    mycursor.execute(query)
    rows = mycursor.fetchall()
    lines = []
    for row in rows:
        load = dict(zip(columns, row))

        load_id = ''.join([str(load[field]) for field in columns if field != 'load_key'])
        if load_id in loads:
            loads[load_id]['load_key'] = load['load_key']

    if not insert_new:
        return loads

    for key, load in loads.items():
        if 'load_key' not in load:
            lines.append(tuple([load[field] for field in columns[1:]]))

    insert_sql = f"INSERT INTO load_d(contracted_indicator, cancelled_indicator, booked_indicator, sourced_indicator) VALUES (%s, %s, %s, %s)"

    if len(lines) > 0:
        mycursor.executemany(insert_sql, lines)
        mydb.commit()
        print(mycursor.rowcount, "was inserted.")
    else:
        print('Nothing new')

    return get_load_ids(loads)


def get_tracking_ids(trackings, insert_new=False):
    columns = [
        'tracking_key',
        'mobile_app_indicator',
        'macro_point_indicator',
        'edi_indicator'
    ]

    query = f"""SELECT tracking_key, mobile_app_indicator, macro_point_indicator, edi_indicator FROM tracking_d"""
    mycursor.execute(query)
    rows = mycursor.fetchall()
    lines = []
    for row in rows:
        tracking = dict(zip(columns, row))

        tracking_id = ''.join([str(value) for key, value in tracking.items() if key != 'tracking_key'])

        if tracking_id in trackings:
            trackings[tracking_id]['tracking_key'] = tracking['tracking_key']

    if not insert_new:
        return trackings

    for key, tracking in trackings.items():
        if 'tracking_key' not in tracking:
            lines.append(tuple([value for k, value in tracking.items()]))

    insert_sql = f"INSERT INTO tracking_d(mobile_app_indicator, macro_point_indicator, edi_indicator) VALUES (%s, %s, %s)"

    if len(lines) > 0:
        mycursor.executemany(insert_sql, lines)
        mydb.commit()
        print(mycursor.rowcount, "was inserted.")
    else:
        print('Nothing new')

    return get_tracking_ids(trackings)


def get_lane_ids(lanes, insert_new=False):
    columns = [
        'lane_key',
        'origin_city',
        'origin_state',
        'origin_country',
        'mileage',
        'destination_city',
        'destination_state',
        'destination_country',
        'city_pair'
    ]

    query = f"""SELECT lane_key, origin_city, origin_state, origin_country, mileage, destination_city, destination_state, destination_country, city_pair FROM lane_d"""
    mycursor.execute(query)
    rows = mycursor.fetchall()
    lines = []
    for row in rows:
        lane = dict(zip(columns, row))
        lane_id = ''.join([str(value) for key, value in lane.items() if key != 'lane_key'])
        if lane_id in lanes:
            lanes[lane_id]['lane_key'] = lane['lane_key']

    if not insert_new:
        return lanes

    for key, lane in lanes.items():
        if 'lane_key' not in lane:
            lines.append(tuple([lane[field] for field in columns[1:]]))

    insert_sql = f"INSERT INTO lane_d(origin_city, origin_state, origin_country, mileage, destination_city, destination_state, destination_country, city_pair) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    if len(lines) > 0:
        mycursor.executemany(insert_sql, lines)
        mydb.commit()
        print(mycursor.rowcount, "was inserted.")
    else:
        print('Nothing new')

    return get_lane_ids(lanes)


def get_shipper_ids(shippers, insert_new=False):

    columns = [
        'shipper_key',
        'shipper_name',
    ]

    shippers_name = tuple([shipper for shipper in shippers])
    query = f"""SELECT shipper_key, shipper_name FROM shipper_d WHERE
    shipper_name in {shippers_name}
    """
    mycursor.execute(query)
    rows = mycursor.fetchall()
    lines = []
    shippers_mapping = {}

    for row in rows:
        shipper = dict(zip(columns, row))

        shipper_id = shipper['shipper_name']

        if shipper_id in shippers:
            shippers_mapping[shipper_id] = shipper

    if not insert_new:
        return shippers_mapping

    for shipper in shippers:
        if shipper not in shippers_mapping:
            lines.append((shipper,))

    insert_sql = f"INSERT INTO shipper_d (shipper_name) VALUES (%s)"

    if len(lines) > 0:
        mycursor.executemany(insert_sql, lines)
        mydb.commit()
        print(mycursor.rowcount, "was inserted.")
    else:
        print('Nothing new')

    return get_shipper_ids(shippers)


def insert_facts(facts):
    columns = [
        'quote_date',
        'quote_time',
        'book_date',
        'book_time',
        'source_date',
        'source_time',
        'pickup_appointment_date',
        'pickup_appointment_time',
        'pickup_date',
        'pickup_time',
        'delivery_appointment_date',
        'delivery_appointment_time',
        'delivery_date',
        'delivery_time',
        'lane_key',
        'book_price',
        'source_price',
        'profit_and_loss',
        'shipper_key',
        'carrier_key',
        'on_time_key',
        'sourcing_channel_key',
        'equipment_type_key',
        'load_key',
        'tracking_key'
    ]
    s = ['%s'] * len(columns)
    insert_sql = f"INSERT INTO truck_run_f({', '.join(columns)}) VALUES ({', '.join(s)})"

    lines = []
    for fact in facts:
        lines.append(tuple([fact[field] for field in columns]))

    if len(facts) > 0:
        mycursor.executemany(insert_sql, lines)
        mydb.commit()
        print(mycursor.rowcount, "was inserted.")
    else:
        print('Nothing new')

    return None
