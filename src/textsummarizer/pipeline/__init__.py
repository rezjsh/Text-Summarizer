from textsummarizer.components.data_acquisition import DataAcquisition
from textsummarizer.logging import logger
from textsummarizer.config.configuration import ConfigHandler


config = ConfigHandler()


class DataAcquisitionPipeline:
    def main(self):
        data_acquisition = config.get_data_acquisition_config()
        data_acquisition.download_file()
        data_acquisition.extract_zip_file()



class DataVerificationPipeline:
    def main(self):
        data_verification = config.get_data_verification_config()
        data_verification.verify_all_files_exist()
        data_verification.get_csv_files_info()


class DataTransformationPipeline:
    def main(self):
        data_transformation = config.get_data_transformation_config()
        data_transformation.convert()