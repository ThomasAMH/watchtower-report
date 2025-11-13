from pathlib import Path
import json
import pandas as pd
from concurrent.futures import ThreadPoolExecutor


def main():
    """
    Read in all the data from the input directories into the program_data directory,
    cleaned and formatted.
    Move read input items into the read_data directory in a subdirectory by date.
    Could be made faster with threading...
    """

    # Constants
    PROGRAM_DATA_META_FILE = Path(".\\program_data\\meta_data.json\\")
    INPUT_DATA_DIR = Path(".\\input_data\\")
    HEADERS_CONFIG_FILE = Path(".\\config\\headers.json")

    # Check if meta file exists and confirm overwrite
    if PROGRAM_DATA_META_FILE.exists():
        with open(PROGRAM_DATA_META_FILE, 'r', encoding='utf-8-sig') as metafile:
            meta_data = json.load(metafile)
        user_input = print(f"Are you sure you want to overwrite the data from {meta_data['last_input_date']}? (y/n): ")
        if user_input.lower() != 'y':
            print("Exiting without changes.")
            return

    # Delete all .json files in program data that are not the meta file
        prep_directories(PROGRAM_DATA_META_FILE, INPUT_DATA_DIR)

    # Load headers configuration
    with open(HEADERS_CONFIG_FILE, 'r', encoding='utf-8-sig') as headerfile:
        headers_config = json.load(headerfile)

    # Process each input data directory

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_input_directory, input_dir, headers_config[input_dir.name])
                   for input_dir in INPUT_DATA_DIR.iterdir() if input_dir.is_dir() and input_dir.name in headers_config]

        print("Processing input data directories with threading...")

        all_results = [future.result() for future in futures]

    # Combine metadata from all directories
    meta_data = {'last_input_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
    for result in all_results:
        meta_data.update(result)

    # Write metadata
    with open(PROGRAM_DATA_META_FILE, 'w', encoding='utf-8-sig') as metafile:
        json.dump(meta_data, metafile, indent=4)


def process_input_directory(input_dir: Path, headers: dict) -> dict:
    """
    Process all files in the given input directory and return cleaned data as a list of dictionaries.
    """
    meta_data = {}
    output_data = []

    for input_file in input_dir.iterdir():
        if input_file.suffix.lower() in ['.xls', '.xlsx']:
            output_data += read_excel_data(input_file, headers)
        elif input_file.suffix.lower() == '.csv':
            output_data += read_csv_data(input_file, headers)
        meta_data.update({input_file.name: len(output_data)})
        print(f"    Read {len(output_data):,} records from {input_file.name}")

    # Write cleaned data to program data directory
    if len(output_data) == 0:
        return meta_data

    output_file = Path(f".\\program_data\\{input_dir.name}_data.json")
    with open(output_file, 'w', encoding='utf-8') as outfile:
        return_obj = {}
        for order_data in output_data:
            order_number = order_data['order_number']
            if order_number not in return_obj:
                return_obj.update({order_data['order_number']: order_data})
        json.dump(return_obj, outfile, indent=4)

    return meta_data


def read_excel_data(file_path: Path, headers: dict) -> list:
    """
    Read data from an Excel file and return a list of dictionaries containing only the required headers.
    """
    needed_headers = [key for key in headers.keys()]
    try:
        df = pd.read_excel(file_path, dtype=str)
        cleaned_data = df[needed_headers].rename(columns=headers)
        cleaned_data['order_number'] = cleaned_data['order_number'].apply(clean_order_number)
        return cleaned_data.to_dict(orient='records')
    except KeyError as e:
        print(f"Error reading {file_path.name}: Missing required headers. Please check the headers config file: {e}")
        return []


def read_csv_data(file_path: Path, headers: dict) -> list:
    """
    Read data from a csv file and return a list of dictionaries containing only the required headers.
    """
    needed_headers = [key for key in headers.keys()]
    try:
        df = pd.read_csv(file_path, dtype=str)
        cleaned_data = df[needed_headers].rename(columns=headers)
        cleaned_data['order_number'] = cleaned_data['order_number'].apply(clean_order_number)
        return cleaned_data.to_dict(orient='records')

    except KeyError as e:
        print(f"Error reading {file_path.name}: Missing required headers. Please check the headers config file: {e}")
        return []


def clean_order_number(order_number: str) -> str:
    """
    Clean the order number by removing unwanted characters and formatting it.
    """
    cleaned = order_number.replace("_DOTERRA", "").replace("DT", "")
    return cleaned


def prep_directories(PROGRAM_DATA_META_FILE, INPUT_DATA_DIR):
    """
    Prepare program data directory by clearing old data files except meta file.
    """
    # Delete all .json files in program data that are not the meta file
    for file in Path(INPUT_DATA_DIR).glob("*.json"):
        if file != PROGRAM_DATA_META_FILE:
            file.unlink()


if __name__ == "__main__":
    main()
