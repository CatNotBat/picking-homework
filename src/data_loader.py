import numpy as np
from scipy.io import loadmat
from typing import Tuple


def load_seismic_data(file_path: str) -> Tuple[np.ndarray, float, np.ndarray]:
    """
    Loads seismic data from a .mat file.

    Args:
        file_path: The file path to the .mat file.

    Returns:
        A tuple of:
            - seismic_data (np.ndarray)
            - sampling_frequency (float)
            - geometry (np.ndarray)
    """
    mat_data = loadmat(file_path, squeeze_me=True)

    seismic_data_array = np.asarray(mat_data["data"])
    sampling_frequency = float(mat_data["fs"])
    geometry = np.asarray(mat_data["geometry"])

    seismic_data_array = seismic_data_array.T

    return seismic_data_array, sampling_frequency, geometry
