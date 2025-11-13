import csv
import json

def main():
    """
    Read in a csv file called transit times from this directory and update the transit_times.json file with the data
    Will override the data in the transit_times.json file with the data from the csv
    Last run: 2025-11-12
    """
    # Define constants
    COUNTRY_HEADER = "Country"
    SHIP_Q_HEADER = "Ship Q"
    TRANSIT_TIME_AVG_HEADER = "Transit Time"
    FILE_NAME = ".\\src\\update_config\\transit_times.csv"

    with open(FILE_NAME, mode='r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        transit_times = {}
        for row in reader:
            country = row[COUNTRY_HEADER].strip().lower()
            ship_q = row[SHIP_Q_HEADER].strip().lower()
            transit_time_avg = row[TRANSIT_TIME_AVG_HEADER].strip()

            if country not in transit_times:
                transit_times[country] = {}

            transit_times[country][ship_q] = transit_time_avg
    with open('.\\config\\transit_times.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(transit_times, jsonfile, indent=4)


if __name__ == "__main__":
    main()