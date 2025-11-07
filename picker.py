import numpy as np
from strategies.base_strategy import BasePickingStrategy


class SeismicPicker:
    """A class to perform seismic data picking using a specified strategy.

    Args:
        strategy (BasePickingStrategy): The picking algorithm (strategy)
            to be used by this picker.

    Attributes:
        _strategy (BasePickingStrategy): The stored picking strategy object.
    """

    def __init__(self, strategy: BasePickingStrategy):
        self._strategy = strategy

    def run_picking(self, data: np.ndarray) -> np.ndarray:
        """Executes the loaded picking strategy on the seismic data.

        Args:
            data (np.ndarray): The 2D seismic data array, with
                               shape (num_samples, num_traces).

        Returns:
            np.ndarray: A 1D array of integers containing the pick
                        index (sample number) for each trace.
        """
        return self._strategy.pick(data)
