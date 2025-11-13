from pathlib import Path
import pandas as pd


def main():
    """
    Clean and format the data in program_data directory
    based on the headers configuration.
    """
    clean_dtx_data()
    clean_on_hold_data()


def clean_dtx_data():
    """
    Clean and format DTX data files by adding countries,
    categorizing ship_via     
    """
    df = pd.read_csv(Path(".\\program_data\\dataextract_data.csv"), encoding='utf-8-sig')
    country_dict = {"DEU": "germany",
                    "ITA": "italy",
                    "POL": "poland",
                    "GBR": "uk",
                    "UKR": "ukraine",
                    "ISR": "israel",
                    "FRA": "france"}

    # If country is in country dict, update, else: addr_line_3
    def switch_country(row):
        if row['ship_to_country'] in country_dict:
            return country_dict[row['ship_to_country']]
        else:
            return row['ship_to_addr_3'].lower()

    df['ship_to_country'] = df.apply(switch_country, axis=1)

    # Drop "ship_to_addr_3"
    df = df.drop(columns=['ship_to_addr_3'])

    # Stadardize "ship_via" column
    def categorize_ship_via(value):
        if value.lower().find("stan") != -1:
            return "standard"
        elif value.lower().find("prem") != -1:
            return "premium"
        else:
            return "other"
    df['ship_via'] = df['ship_via'].apply(categorize_ship_via)

    # Clean order type: only keep first character
    df['order_status'] = df['order_status'].apply(lambda x: x[0])

    df.to_csv(Path(".\\program_data\\dataextract_data.csv"), index=False, encoding='utf-8-sig')


def clean_on_hold_data():
    """
    Clean and format On Hold data files.
    """
    df = pd.read_csv(Path(".\\program_data\\on_hold_data.csv"), encoding='utf-8-sig')

    df['ship_to_country'] = df['ship_to_address'].apply(lambda x: x[-2:])
    df = df.drop(columns=['ship_to_address'])

    df.to_csv(Path(".\\program_data\\on_hold_data.csv"), index=False, encoding='utf-8-sig')


def clean_unshipped_orders_data():
    """
    Clean and format Unshipped Orders data files.
    """
    df = pd.read_csv(Path(".\\program_data\\unshipped_orders_data.csv"), encoding='utf-8-sig')

    df['ship_to_country'] = df['ship_to_address'].apply(lambda x: x[-2:])
    df = df.drop(columns=['ship_to_address'])

    df.to_csv(Path(".\\program_data\\unshipped_orders_data.csv"), index=False, encoding='utf-8-sig')


if __name__ == "__main__":
    main()
