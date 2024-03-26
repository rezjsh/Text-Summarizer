import os
import urllib.request as request
import zipfile
from textsummarizer.logging import logger
from textsummarizer.utils.common import get_size
from textsummarizer.entity import DataIngestionConfig
from pathlib import Path


class DataIngestion:
    def __init__(self, config:DataIngestionConfig):
        self.config = config

    def download_file(self):
        """
        Downloads a file from the specified URL to the local directory if it does not already exist.

        Args:
            self: The object instance.
        
        Returns:
            None
        """
        if not os.path.exists(self.config.local_data_file):
            # Download the file from the source URL to the local directory
            filename, headers = request.urlretrieve(
                url=self.config.source_url,
                filename=self.config.local_data_file
            )
            logger.info(f"{filename} downloaded! with the following info: \n{headers}")
        else:
            # Log a message if the file already exists
            logger.info(f"File already exists with a size of: {get_size(Path(self.config.local_data_file))}")


    def extract_zip_file(self):
        """
        Extracts the contents of a zip file to the specified directory.

        Args:
            self: The object instance.
        
        Returns:
            None
        """
        # Create the directory if it does not exist
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        
        # Extract the zip file contents to the specified directory
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)

