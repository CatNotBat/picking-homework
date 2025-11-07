from typing import Tuple
import numpy as np
from scipy.io import loadmat


def load_seismic_data(file_path: str) -> Tuple[np.ndarray, float, np.ndarray]:
    """
    Loads seismic data from a .mat file.

    Args:
        file_path: The file path to the .mat file.

    Returns:
        A tuple of:
            - seismic_data (np.ndarray): The 2D seismic data array.
            - sampling_frequency (float): The data's sampling frequency (e.g., 1000.0).
            - geometry (np.ndarray): The sensor geometry information.
    """
    mat_data = loadmat(file_path, squeeze_me=True)

    seismic_data_array = mat_data["data"]
    sampling_frequency = float(mat_data["fs"])
    geometry = mat_data["geometry"]

    return seismic_data_array, sampling_frequency, geometry
