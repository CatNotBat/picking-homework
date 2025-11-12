import numpy as np
from scipy.signal import lfilter
from strategies.base_strategy import BasePickingStrategy
from analysis import calculate_distances_from_source


class ModelDrivenSTALTAStrategy(BasePickingStrategy):
    GOOD_WINDOW_SAMPLE_RANGE = 20
    SEARCH_WINDOW_RADIUS = 40

    def __init__(
        self,
        short_window: int = 20,
        long_window: int = 200,
        ratio_threshold: float = 3.0,
    ):
        self._short_window = short_window
        self._long_window = long_window
        self._ratio_threshold = ratio_threshold

    def pick(self, data: np.ndarray, geometry: np.ndarray) -> np.ndarray:
        """Performs first-break picking using the STA/LTA method combined with
        attempting to fit a polynomal on top of data we got, then a small
        STA/LTA at the end.

        Args:
            data (np.ndarray)
            short_window (int)
            long_window (int)
            ratio_threshold (float)
        """

        unfilterd_first_break_indices = self._run_basic_sta_lta(data)
        all_distances = calculate_distances_from_source(
            geometry, unfilterd_first_break_indices
        )
        valid_picks = unfilterd_first_break_indices[unfilterd_first_break_indices > -1]
        if not valid_picks.size > 0:
            return unfilterd_first_break_indices

        min_valid_pick = np.min(valid_picks)

        good_mask = (unfilterd_first_break_indices > -1) & (
            unfilterd_first_break_indices
            < (min_valid_pick + self.GOOD_WINDOW_SAMPLE_RANGE)
        )
        clean_distances = all_distances[good_mask]
        clean_indices = unfilterd_first_break_indices[good_mask]

        try:
            model_coeffs = np.polyfit(clean_distances, clean_indices, 2)
            predicted_indices = np.polyval(model_coeffs, all_distances).astype(int)

            final_picks = self._run_model_driven_search(
                data, predicted_indices, self.SEARCH_WINDOW_RADIUS
            )

            return final_picks
        except np.linalg.LinAlgError:
            return unfilterd_first_break_indices

    def _run_basic_sta_lta(self, data: np.ndarray) -> np.ndarray:
        _, num_traces = data.shape
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

    def _run_model_driven_search(
        self, data: np.ndarray, predicted_indices: np.ndarray, search_window_radius: int
    ) -> np.ndarray:
        num_samples, num_traces = data.shape
        final_picks = -1 * np.ones(num_traces, dtype=int)
        stable_search_start = self._long_window

        for trace_idx in range(num_traces):
            predicted_index = predicted_indices[trace_idx]
            window_start = max(
                stable_search_start, predicted_index - search_window_radius
            )
            window_end = min(num_samples, predicted_index + search_window_radius)

            if window_start >= window_end:
                continue

            trace = data[:, trace_idx]
            sta_lta_ratio = self._compute_sta_lta(trace)
            ratio_in_window = sta_lta_ratio[window_start:window_end]
            peak_ratio_in_window = np.max(ratio_in_window)
            if peak_ratio_in_window > self._ratio_threshold:
                pick_in_window_idx = np.argmax(ratio_in_window)
                final_picks[trace_idx] = window_start + pick_in_window_idx

        return final_picks

    def _compute_sta_lta(self, trace: np.ndarray) -> np.ndarray:
        abs_trace = np.abs(trace)
        epsilon = 1e-15
        b_sta = np.ones(self._short_window) / self._short_window
        b_lta = np.ones(self._long_window) / self._long_window

        sta = lfilter(b_sta, [1], abs_trace)
        lta = lfilter(b_lta, [1], abs_trace)

        ratio = sta / (lta + epsilon)

        return ratio
