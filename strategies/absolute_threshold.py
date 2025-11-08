import numpy as np
from strategies.base_strategy import BasePickingStrategy


class AbsoluteThresholdStrategy(BasePickingStrategy):
    """A picking strategy that normalizes each trace by its peak-to-trough
    amplitude and applies a absolute threshold to determine first-break picks.

    Args:
        threshold (float): The absolute threshold value.

    Methods:
        pick(data: np.ndarray) -> np.ndarray:
            Implements the picking algorithm.
    """

    def __init__(self, threshold: float = 1e-9):
        self._threshold = threshold

    def pick(self, data: np.ndarray) -> np.ndarray:
        """Performs first-break picking using the relative threshold method.

        Args:
            data (np.ndarray): The 2D seismic data array, with
                               shape (num_samples, num_traces).

        Returns:
            np.ndarray: A 1D array of integers containing the pick
                        index (sample number) for each trace.
        """
        first_break_indices = self._find_first_break_indices(data)
        return first_break_indices

    def _find_first_break_indices(self, data: np.ndarray) -> np.ndarray:
        abs_data = np.abs(data)
        crossed_threshold = abs_data > self._threshold
        failed_trace_mask = ~np.any(crossed_threshold, axis=0)
        pick_indices = np.argmax(crossed_threshold, axis=0).astype(int)
        pick_indices[failed_trace_mask] = -1
        return pick_indices
