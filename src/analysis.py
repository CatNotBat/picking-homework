import numpy as np


def convert_indices_to_time(indices: np.ndarray, fs: float) -> np.ndarray:
    pick_times_ms = indices.astype(float) / fs * 1000.0
    pick_times_ms[indices == -1] = np.nan
    return pick_times_ms
