import numpy as np
from scipy.signal import lfilter
from strategies.base_strategy import BasePickingStrategy


class STA_LTAStrategy(BasePickingStrategy):
    def __init__(
        self,
        short_window: int = 20,
        long_window: int = 200,
        ratio_threshold: float = 3.0,
    ):
        self._short_window = short_window
        self._long_window = long_window
        self._ratio_threshold = ratio_threshold

    def pick(self, data: np.ndarray) -> np.ndarray:
        """Performs first-break picking using the STA/LTA method.

        Args:
            data (np.ndarray)
            short_window (int)
            long_window (int)
            ratio_threshold (float)
        """

        first_break_indices = self._find_first_break_indices(data)
        return first_break_indices

    def _find_first_break_indices(self, data: np.ndarray) -> np.ndarray:
        num_samples, num_traces = data.shape
        pick_indices = -1 * np.ones(num_traces, dtype=int)
        search_start_index = self._long_window

        for trace_idx in range(num_traces):
            trace = data[:, trace_idx]
            sta_lta_ratio = self._compute_sta_lta(trace)[search_start_index:]
            if np.any(sta_lta_ratio > self._ratio_threshold):
                crossed_threshold = sta_lta_ratio > self._ratio_threshold
                first_break = np.argmax(crossed_threshold)
                pick_indices[trace_idx] = first_break + search_start_index

        return pick_indices

    def _compute_sta_lta(self, trace: np.ndarray) -> np.ndarray:
        abs_trace = np.abs(trace)
        epsilon = 1e-15
        b_sta = np.ones(self._short_window) / self._short_window
        b_lta = np.ones(self._long_window) / self._long_window

        sta = lfilter(b_sta, [1], abs_trace)
        lta = lfilter(b_lta, [1], abs_trace)

        ratio = sta / (lta + epsilon)

        return ratio
