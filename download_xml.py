import os
import csv
import requests
import time


def download_files(csv_path, output_dir):
    """
    Downloads files from URLs specified in a CSV file and saves them with custom names.

    Parameters:
    - csv_path (str): Path to the CSV file containing names and URLs.
    - output_dir (str): Directory where the downloaded files will be saved.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(csv_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader, None)  # Skip the header row
        for row in reader:
            if len(row) < 2:
                print(f"Skipping invalid row: {row}")
                continue

            file_name, url = row[0], row[1]
            output_file = os.path.join(output_dir, f"{file_name}.xml")

            print(f"Downloading {file_name} from {url}...")
            start_time = time.time()
            try:
                response = requests.get(url, timeout=30)
                response.raise_for_status()  # Raise an error for bad HTTP status codes
                with open(output_file, 'wb') as file:
                    file.write(response.content)
                elapsed_time = time.time() - start_time
                print(f"Successfully downloaded {file_name}. Time taken: {elapsed_time:.2f} seconds.")
            except requests.exceptions.RequestException as e:
                print(f"Failed to download {file_name} from {url}. Error: {e}")


if __name__ == "__main__":
    CSV_PATH = "urls.csv"
    OUTPUT_DIR = "xml_files"
    download_files(CSV_PATH, OUTPUT_DIR)
