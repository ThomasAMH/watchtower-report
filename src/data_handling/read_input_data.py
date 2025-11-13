from pathlib import Path
import json
import pandas as pd


def main():
    """
    Read in all the data from the input directories into the program_data directory,
    cleaned and formatted.
    Move read input items into the read_data directory in a subdirectory by date.
    Could be made faster with threading...
    """

    PROGRAM_DATA_META_FILE = Path(".\\program_data\\meta_data.json\\")
    INPUT_DATA_DIR = Path(".\\input_data\\")
    HEADERS_CONFIG_FILE = Path(".\\config\\headers.json")

    if PROGRAM_DATA_META_FILE.exists():
        with open(PROGRAM_DATA_META_FILE, 'r', encoding='utf-8-sig') as metafile:
            meta_data = json.load(metafile)
        user_input = input(f"Are you sure you want to overwrite the data from {meta_data['last_input_date']}? (y/n): ")
        if user_input.lower() != 'y':
            print("Exiting without changes.")
            return

    # Remove all .csv files in program data that are not the meta file
    for file in Path(".\\program_data\\").glob("*.csv"):
        if file != PROGRAM_DATA_META_FILE:
            file.unlink()

    # Load headers configuration
    with open(HEADERS_CONFIG_FILE, 'r', encoding='utf-8-sig') as headerfile:
        headers_config = json.load(headerfile)

    # Process each input data directory
    meta_data = {}
    for input_dir in INPUT_DATA_DIR.iterdir():
        if not input_dir.is_dir():
            continue
        input_name = input_dir.name
        meta_data.update({input_name: {}})
        if input_name in headers_config:
            headers = headers_config[input_name]
            print(f"Processing input from {input_name}")

            output_data = []
            for input_file in input_dir.iterdir():
                if input_file.suffix.lower() in ['.xls', '.xlsx']:
                    output_data.append(read_excel_data(input_file, headers))
                elif input_file.suffix.lower() == '.csv':
                    output_data.append(read_csv_data(input_file, headers))
                print(f"    Read {output_data[-1].shape[0]:,} records from {input_file.name}")
                meta_data[input_name].update({input_file.name: len(output_data)})

            # Write cleaned data to program data directory
            if len(output_data) == 0:
                continue

            output_file = Path(f".\\program_data\\{input_name}_data.csv")
            with open(output_file, 'w', encoding='utf-8') as outfile:
                pd.concat(output_data).to_csv(outfile, index=False, lineterminator='\n')
                # return_obj = {}
                # for order_data in output_data:
                #     order_number = order_data['order_number']
                #     if order_number not in return_obj:
                #         return_obj.update({order_data['order_number']: order_data})
                # json.dump(return_obj, outfile, indent=4)

    with open(PROGRAM_DATA_META_FILE, 'w', encoding='utf-8-sig') as metafile:
        meta_data.update({'last_input_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')})
        json.dump(meta_data, metafile, indent=4)


def read_excel_data(file_path: Path, headers: dict) -> pd.DataFrame:
    """
    Read data from an Excel file and return a list of dictionaries containing only the required headers.
    """
    needed_headers = [key for key in headers.keys()]
    try:
        df = pd.read_excel(file_path, dtype=str)
        cleaned_data = df[needed_headers].rename(columns=headers)
        cleaned_data['order_number'] = cleaned_data['order_number'].apply(clean_order_number)
        return cleaned_data
    except KeyError as e:
        print(f"Error reading {file_path.name}: Missing required headers. Please check the headers config file: {e}")
        return pd.DataFrame()


def read_csv_data(file_path: Path, headers: dict) -> pd.DataFrame:
    """
    Read data from a csv file and return a list of dictionaries containing only the required headers.
    """
    needed_headers = [key for key in headers.keys()]
    try:
        df = pd.read_csv(file_path, dtype=str)
        cleaned_data = df[needed_headers].rename(columns=headers)
        cleaned_data['order_number'] = cleaned_data['order_number'].apply(clean_order_number)
        return cleaned_data

    except KeyError as e:
        print(f"Error reading {file_path.name}: Missing required headers. Please check the headers config file: {e}")
        return pd.DataFrame()


def clean_order_number(order_number: str) -> str:
    """
    Clean the order number by removing unwanted characters and formatting it.
    """
    cleaned = order_number.replace("_DOTERRA", "").replace("DT", "")
    return cleaned


if __name__ == "__main__":
    main()
