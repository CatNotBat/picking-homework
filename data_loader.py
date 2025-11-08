import numpy as np
from scipy.io import loadmat
from typing import Tuple, Dict, Any


def load_seismic_data(file_path: str) -> Tuple[np.ndarray, float, np.ndarray]:
    """
    Loads seismic data from a .mat file.

    Args:
        file_path: The file path to the .mat file.

    Returns:
        A tuple of:
            - seismic_data (np.ndarray): The 2D seismic data array
                                         in (num_samples, num_traces) format.
            - sampling_frequency (float): The data's sampling frequency.
            - geometry (np.ndarray): The sensor geometry information.
    """
    mat_data: Dict[str, Any] = loadmat(file_path, squeeze_me=True)

    seismic_data_array: np.ndarray = np.asarray(mat_data["data"])
    sampling_frequency: float = float(mat_data["fs"])
    geometry: np.ndarray = np.asarray(mat_data["geometry"])

    # The data is saved as (num_traces, num_samples).
    # We transpose it to the standard (num_samples, num_traces)
    # format for the rest of the application.
    seismic_data_array = seismic_data_array.T

    return seismic_data_array, sampling_frequency, geometry
