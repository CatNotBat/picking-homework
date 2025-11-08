import numpy as np
from strategies.base_strategy import BasePickingStrategy


class SeismicPicker:
    DISPLAY_TITLE = "Seismographic Preview of First Breaks"
    """A class to perform seismic data picking using a specified strategy.

    Args:
        strategy (BasePickingStrategy): The picking algorithm (strategy)
            to be used by this picker.
        sampling_frequency (float): The sampling frequency of the seismic data.

    Attributes:
        _strategy (BasePickingStrategy): The stored picking strategy object.
        _sampling_frequency (float): The sampling frequency of the seismic data.
    """

    def __init__(self, strategy: BasePickingStrategy, sampling_frequency: float):
        self._strategy = strategy
        self._sampling_frequency = sampling_frequency

    def run_picking(self, data: np.ndarray) -> np.ndarray:
        """Executes the loaded picking strategy on the seismic data.

        Args:
            data (np.ndarray): The 2D seismic data array, with
                               shape (num_samples, num_traces).

        Returns:
            np.ndarray: A 1D array of integers containing the pick
                        index (sample number) for each trace.
        """
        first_breaks_indices = self._strategy.pick(data)
        return first_breaks_indices
