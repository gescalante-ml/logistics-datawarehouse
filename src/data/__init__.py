headers = ['loadsmart_id', 'lane', 'quote_date', 'book_date', 'source_date', 'pickup_date', 'delivery_date',
           'book_price', 'source_price', 'pnl', 'mileage', 'equipment_type', 'carrier_rating', 'sourcing_channel',
           'vip_carrier', 'carrier_dropped_us_count', 'carrier_name', 'shipper_name', 'carrier_on_time_to_pickup',
           'carrier_on_time_to_delivery', 'carrier_on_time_overall', 'pickup_appointment_time',
           'delivery_appointment_time', 'has_mobile_app_tracking', 'has_mobile_app_tracking', 'has_macropoint_tracking',
           'has_edi_tracking', 'contracted_load', 'load_booked_autonomously', 'load_sourced_autonomously',
           'load_was_cancelled']

equipment_type = {
    "DRV": 2,
    "RFR": 3,
    "FBE": 4
}

sourcing_channel = {'carrier_capacity': 2,
                    'ts_in': 3,
                    'ts_out': 4,
                    'source_list': 5,
                    'dat_out': 6,
                    'dat_in': 7,
                    'livejobs': 8,
                    'external_source_list': 9
                    }
