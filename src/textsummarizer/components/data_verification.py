import os
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
import pandas as pd


@dataclass(frozen=True)
class DataVerification:
    root_dir: Path
    STATUS_FILE: str
    INFO_FILE: str
    ALL_REQUIRED_FILES: list


    def verify_all_files_exist(self)-> bool:
        try:
            verification_status = None

            all_files = os.listdir(os.path.join("artifacts","data_acquisition","samsum_dataset"))

            for file in all_files:
                if file not in self.ALL_REQUIRED_FILES:
                    verification_status = False
                    with open(self.STATUS_FILE, 'w') as f:
                        f.write(f"Verification status: {verification_status}")
                else:
                    verification_status = True
                    with open(self.STATUS_FILE, 'w') as f:
                        f.write(f"Verification status: {verification_status}")

            return verification_status
        
        except Exception as e:
            raise e

    def get_csv_files_info(self):
        try:
            folder_path = os.path.join("artifacts", "data_acquisition")
            with open(self.INFO_FILE, 'w') as f:  # Open the file in write mode to clear previous content
                f.write("CSV File Metadata:\n")

            for file_name in os.listdir(folder_path):
                if file_name.endswith('.csv'):
                    file_path = os.path.join(folder_path, file_name)
                    file_size = os.path.getsize(file_path)

                    # Read the CSV file using pandas to extract additional metadata
                    df = pd.read_csv(file_path)
                    num_rows = len(df)
                    data_types = df.dtypes
                    

                    # Get the creation/modification date of the file
                    modification_time = os.path.getmtime(file_path)
                    modification_date = datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d %H:%M:%S')

                    with open(self.INFO_FILE, 'a') as f:  # Open the file in append mode to add metadata
                        f.write(f"File Name: {file_name}\n")
                        f.write(f"File Size: {file_size} bytes\n")
                        f.write(f"Number of Rows: {num_rows}\n")
                        f.write(f"Data Types:\n{data_types}\n")
                        f.write(f"Last Modified: {modification_date}\n\n")
                        f.write("************************************")
                        f.write("************************************\n\n\n")
        except Exception as e:
            raise e

  