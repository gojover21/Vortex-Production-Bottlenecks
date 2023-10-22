import pandas as pd
from math import ceil

stations = ['WELDING', 'HYDRO TEST', 'SENSORING', 'FL SCALE A', 'FL SCALE B', 'FL SCALE C', 'FL SCALE D', 'FL SCALE E', 'CONFIG', 'FINAL ASSEMBLY', 'FINAL INSPECTION', 'PACKAGING']

# Define the input data as a dictionary
station_data = {
    'WELDING': {'number_of_stations': 5, 'raw_processing_time': 0.262, 'effective_hrs_per_day': 8, 'yield': 0.99, 'setup_time': 0.03, 'number_between_setups': 1, 'mttf': 40, 'mttr': 0.17},
    'HYDRO TEST': {'number_of_stations': 2, 'raw_processing_time': 0.019, 'effective_hrs_per_day': 8, 'yield': 0.96, 'setup_time': 0.15, 'number_between_setups': 5, 'mttf': 40, 'mttr': 0.17},
    'SENSORING': {'number_of_stations': 1, 'raw_processing_time': 0.025, 'effective_hrs_per_day': 8, 'yield': 0.95, 'setup_time': 0, 'number_between_setups': 5, 'mttf': 40, 'mttr': 0.17},
    'FL SCALE A': {'scale': 'A', 'process_time': 422, 'setup_time': 93, 'total_mins_per_scale': 13769.42, 'yield': 0.98, 'effective_hrs_per_day': 7},
    'FL SCALE B': {'scale': 'B', 'process_time': 2690.54, 'setup_time': 0, 'total_mins_per_scale': 2690.54, 'yield': 0.99, 'effective_hrs_per_day': 6},
    'FL SCALE C': {'scale': 'C', 'process_time': 4981, 'setup_time': 0, 'total_mins_per_scale': 4981, 'yield': 0.96, 'effective_hrs_per_day': 7},
    'FL SCALE D': {'scale': 'D', 'process_time': 2817.23, 'setup_time': 0, 'total_mins_per_scale': 2817.23, 'yield': 0.97, 'effective_hrs_per_day': 8},
    'FL SCALE E': {'scale': 'E', 'process_time': 1210.24, 'setup_time': 0, 'total_mins_per_scale': 1210.24, 'yield': 0.99, 'effective_hrs_per_day': 7},
    'CONFIG': {'number_of_stations': 1, 'raw_processing_time': 0.03, 'effective_hrs_per_day': 8, 'yield': 0.85, 'setup_time': 0, 'number_between_setups': 1, 'mttf': 40, 'mttr': 0.17},
    'FINAL ASSEMBLY': {'number_of_stations': 1, 'raw_processing_time': 0.023, 'effective_hrs_per_day': 8, 'yield': 0.99, 'setup_time': 0, 'number_between_setups': 1, 'mttf': 40, 'mttr': 0.17},
    'FINAL INSPECTION': {'number_of_stations': 1, 'raw_processing_time': 0.015, 'effective_hrs_per_day': 8, 'yield': 0.99, 'setup_time': 0, 'number_between_setups': 1, 'mttf': 99999999, 'mttr': 0},
    'PACKAGING': {'number_of_stations': 1, 'raw_processing_time': 0.05, 'effective_hrs_per_day': 8, 'yield': 1, 'setup_time': 0, 'number_between_setups': 1, 'mttf': 99999999, 'mttr': 0},
}

# Calculate performance metrics for each station
for station in stations:
    data = station_data[station]
    num_stations = data.get('number_of_stations', 1)
    raw_processing_time = data.get('raw_processing_time', 0)  # set to 0 if not defined
    effective_hrs_per_day = data['effective_hrs_per_day']
    yield_rate = data['yield']
    setup_time = data.get('setup_time', 0)
    num_between_setups = data.get('number_between_setups', 1)
    mttf = data.get('mttf', 99999999)
    mttr = data.get('mttr', 0)

    processing_time = raw_processing_time  # Define processing time for all stations except FINAL INSPECTION and PACKAGING

    # Check if station is FINAL INSPECTION or PACKAGING and adjust processing time accordingly
    if station == 'FINAL INSPECTION':
        buffer_time = 0.017  # buffer time in hours
        processing_time = buffer_time + raw_processing_time
    elif station == 'PACKAGING':
        buffer_time = 0.02  # buffer time in hours
        processing_time = buffer_time + raw_processing_time

    utilization = (num_stations * processing_time) / (effective_hrs_per_day * 60)
    throughput = num_stations * effective_hrs_per_day * yield_rate
    cycle_time = processing_time + setup_time + (num_between_setups - 1) * mttf + mttr
    queue_time = cycle_time - processing_time - setup_time
    wip_in_queue = throughput * queue_time / 60

    # Calculate and print performance metrics
    wip = throughput * cycle_time / 60
    cumulative_cycle_time = cycle_time
    cumulative_wip = wip

    print(f"Station: {station}")
    print(f"Utilization: {utilization:.2%}")
    print(f"Throughput: {throughput:.2f} jobs/hr")
    print(f"Queue Time: {queue_time:.2f} hrs")
    print(f"Cycle Time: {cycle_time:.2f} hrs")
    print(f"Cumulative Cycle Time: {cumulative_cycle_time:.2f} hrs")
    print(f"WIP in Queue: {wip_in_queue:.2f} jobs")
    print(f"WIP: {wip:.2f} jobs")
    print(f"Cumulative WIP: {cumulative_wip:.2f} jobs")
    print()
