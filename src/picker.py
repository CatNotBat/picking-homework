import numpy as np
from strategies.base_strategy import BasePickingStrategy


class SeismicPicker:
    """
    A class to perform seismic data picking using a specified strategy.

    Args:
        strategy (BasePickingStrategy): The picking algorithm (strategy)
            to be used by this picker.
        sampling_frequency (float): The sampling frequency of the seismic data.
    """

    DISPLAY_TITLE = "Seismographic Preview of First Breaks"

    def __init__(self, strategy: BasePickingStrategy, sampling_frequency: float):
        self._strategy = strategy
        self._sampling_frequency = sampling_frequency

    def run_picking(self, data: np.ndarray, gemoetry: np.ndarray) -> np.ndarray:
        """Executes the loaded picking strategy on the seismic data.

        Args:
            data (np.ndarray)

        Returns:
            pick_indices (np.ndarray)
        """
        first_breaks_indices = self._strategy.pick(data, gemoetry)
        return first_breaks_indices
