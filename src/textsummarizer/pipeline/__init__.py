from textsummarizer.components.data_acquisition import DataAcquisition
from textsummarizer.logging import logger
from textsummarizer.config.configuration import ConfigHandler




class DataAcquisitionPipeline:
    def __init__(self):
        self._config = ConfigHandler()
        

    def main(self):
        data_acquisition = self._config.get_data_acquisition_config()
        data_acquisition.download_file()
        data_acquisition.extract_zip_file()