import os
import urllib.request as request
import zipfile
from dataclasses import dataclass
from textsummarizer.logging import logger
from textsummarizer.utils.common import get_size
from pathlib import Path


@dataclass(frozen=True)
class DataAcquisition:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path


    
    def download_file(self):
        """
        Download a file from a specified URL to the local file system.

        Args:
            self: instance of the class containing the source URL and local file path

        Returns:
            None

        Raises:
            Any exceptions that occur during the file download process

        """
        if not os.path.exists(self.local_data_file):  # Check if the file already exists locally
            filename, headers = request.urlretrieve(  # Retrieve the file from the source URL
                url=self.source_URL,
                filename=self.local_data_file
            )
            logger.info(f"{filename} download! with following info: \n{headers}")  # Log the successful download and headers
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.local_data_file))}")  # Log that the file already exists

        
    def extract_zip_file(self):
        """
        Extracts the contents of a zip file to a specified directory.

        Args:
            self: instance of the class containing the local zip file path and the directory to extract to

        Returns:
            None

        Raises:
            Any exceptions that occur during the extraction process

        """
        unzip_path = self.unzip_dir  # Set the path to extract the contents of the zip file
        os.makedirs(unzip_path, exist_ok=True)  # Create the extraction directory if it doesn't exist
        with zipfile.ZipFile(self.local_data_file, 'r') as zip_ref:  # Open the zip file for reading
            zip_ref.extractall(unzip_path)  # Extract all contents of the zip file to the specified directory
