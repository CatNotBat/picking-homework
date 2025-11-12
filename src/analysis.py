import numpy as np


def convert_indices_to_time(indices: np.ndarray, fs: float) -> np.ndarray:
    pick_times_ms = indices.astype(float) / fs * 1000.0
    pick_times_ms[indices == -1] = np.nan
    return pick_times_ms


def calculate_distances_from_source(
    geometry: np.ndarray, pick_indices: np.ndarray
) -> np.ndarray:
    valid_picks = np.where(pick_indices > -1, pick_indices, np.inf)
    source_sensor_index = np.argmin(valid_picks)
    source_coords = geometry[source_sensor_index]
    distances = np.linalg.norm(geometry - source_coords, axis=1)

    return distances


def add_white_noise_to_get_target_snr(
    data: np.ndarray, target_snr: float
) -> np.ndarray:
    peak_signal = np.max(np.abs(data))
    target_noise_peak = peak_signal / target_snr

    white_noise = np.random.normal(0, 1, size=data.shape)
    current_noise_peak = np.max(np.abs(white_noise))
    scaling_factor = target_noise_peak / current_noise_peak
    scaled_noise = white_noise * scaling_factor

    return data + scaled_noise
