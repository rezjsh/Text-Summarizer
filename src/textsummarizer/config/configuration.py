from textsummarizer.constants import *
from textsummarizer.utils.common import read_yaml, create_directories
from textsummarizer.components.data_acquisition import DataAcquisition
from textsummarizer.components.data_verification import DataVerification 

class ConfigHandler:
    def __init__(
        self,
        config_filepath=CONFIG_FILE_PATH,
        params_filepath=PARAMS_FILE_PATH):
        """
        Initialize the ConfigHandler with the provided configuration and parameters file paths.

        Args:
            config_filepath: Path to the configuration file (default: CONFIG_FILE_PATH)
            params_filepath: Path to the parameters file (default: PARAMS_FILE_PATH)

        Returns:
            None

        """
        self.config = self._load_config(config_filepath)  # Load the configuration from the specified file
        self.params = self._load_params(params_filepath)  # Load the parameters from the specified file

        create_directories([self.config.artifacts_root])  # Create necessary directories based on the configuration

    def _load_config(self, config_filepath):
        """
        Load the configuration from the specified YAML file.

        Args:
            config_filepath: Path to the configuration file

        Returns:
            The loaded configuration as a dictionary

        """
        return read_yaml(config_filepath)  # Read and return the configuration from the YAML file

    def _load_params(self, params_filepath):
        """
        Load the parameters from the specified YAML file.

        Args:
            params_filepath: Path to the parameters file

        Returns:
            The loaded parameters as a dictionary

        """
        return read_yaml(params_filepath)  # Read and return the parameters from the YAML file

    def get_data_acquisition_config(self) -> DataAcquisition:
        """
        Get the configuration for data acquisition from the loaded configuration.

        Returns:
            DataAcquisition: An instance of DataAcquisition containing data acquisition configuration

        """
        config = self.config.data_acquisition  # Get the data acquisition configuration from the loaded configuration

        create_directories([config.root_dir])  # Create necessary directories based on the data acquisition configuration

        data_acquisition_config = DataAcquisition(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir
        )  # Create a DataAcquisition instance with the data acquisition configuration

        return data_acquisition_config  # Return the data acquisition configuration



    def get_data_verification_config(self) -> DataVerification:
        """
        Retrieve the data verification configuration.

        This method retrieves the data verification configuration from the provided config, creates necessary directories,
        and returns a DataVerification object.

        Returns:
            DataVerification: An object containing data verification configuration.

        Raises:
            SomeException: Description of the exception raised, if any.
        """
        # Retrieve the data verification configuration from the provided config
        config = self.config.data_verification

        # Create necessary directories
        create_directories([config.root_dir])

        # Create a DataVerification object with the retrieved configuration
        data_verification_config = DataVerification(
            root_dir=config.root_dir,
            STATUS_FILE=config.STATUS_FILE,
            INFO_FILE=config.INFO_FILE,
            ALL_REQUIRED_FILES=config.ALL_REQUIRED_FILES,
        )

        return data_verification_config
