import numpy as np
import matplotlib.pyplot as plt
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
        return self._strategy.pick(data)

    def preview_results(
        self,
        seismic_data: np.ndarray,
        pick_indices: np.ndarray,
    ):
        """
        Generates and displays a "seismographic preview" plot.

        This utility method overlays the calculated pick indices on top
        of the seismic data image, using the correct time and trace axes.

        Args:
            seismic_data (np.ndarray): The 2D seismic data array.
            pick_indices (np.ndarray): The 1D array of pick indices from run_picking().
        """

        num_samples, num_traces = seismic_data.shape
        trace_numbers = np.arange(num_traces)
        pick_times = pick_indices / self._sampling_frequency

        total_time_s = (num_samples - 1) / self._sampling_frequency
        plot_extent = (0, num_traces - 1, total_time_s, 0)

        plt.figure(figsize=(12, 7))
        plt.imshow(
            seismic_data,
            aspect="auto",
            cmap="seismic",
            interpolation="none",
            extent=plot_extent,
        )
        plt.colorbar(label="Amplitude")

        # Plot the picks as a line graph on top
        plt.plot(trace_numbers, pick_times, "k.-", label="First Breaks")
        plt.legend()

        plt.title(self.DISPLAY_TITLE)
        plt.xlabel("Trace Number")
        plt.ylabel("Time (s)")
        plt.show()
