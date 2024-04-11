import os
from box.exceptions import BoxValueError
import yaml
from textsummarizer.logging import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import base64



@ensure_annotations
def read_yaml(path_to_yaml:Path) -> ConfigBox:
    """
    Args:
    path_to_yaml (Path): The path to the YAML file to be read.

    Returns:
        ConfigBox: A ConfigBox object containing the loaded YAML content.

    Raises:
        ValueError: If the YAML file is empty.
        Exception: If an unexpected error occurs during the process.
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"Yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError('Yaml file is empty')
    except Exception as e:
        raise e
    

    
@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """
    Create directories at the specified paths.

    Args:
        path_to_directories (list): A list of paths where directories will be created.
        verbose (bool, optional): Whether to log information about the created directories. Defaults to True.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Created directory at: {path}")



@ensure_annotations
def save_json(path: Path, data: dict):
    """
    Save the given data as a JSON file at the specified path.

    Args:
        path (Path): The path where the JSON file will be saved.
        data (dict): The data to be saved in the JSON file.

    Returns:
        None

    """
    # Open the file at the specified path and write the data as JSON with indentation.
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    
    # Log the information about the saved JSON file.
    logger.info(f"json file saved at {path}")


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """
        Load data from a JSON file and return it as a ConfigBox object.

        Args:
            path (Path): The path to the JSON file.

        Returns:
            ConfigBox: An object containing the data from the JSON file as class attributes instead of a dictionary.
    """
    with open(path) as f:
        content = json.load(f)

    logger.info(f"json file loaded succesfully from: {path}")
    return ConfigBox(content)



@ensure_annotations
def save_bin(data: Any, path: Path):
    """save binary file

    Args:
        data (Any): data to be saved as binary
        path (Path): path to binary file
    """
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at: {path}")




@ensure_annotations
def load_bin(path: Path) -> Any:
    """load binary data

    Args:
        path (Path): path to binary file

    Returns:
        Any: object stored in the file
    """
    data = joblib.load(path)
    logger.info(f"binary file loaded from: {path}")
    return data




@ensure_annotations
def get_size(path: Path) -> str:
    """get size in KB

    Args:
        path (Path): path of the file

    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"



def decodeImage(imgstring, fileName):
    imgdata = base64.b64decode(imgstring)
    with open(fileName, 'wb') as f:
        f.write(imgdata)
        f.close()


def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())