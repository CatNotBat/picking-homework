import numpy as np
import matplotlib.pyplot as plt
from typing import Optional


def plot_wiggles(
    data_block: np.ndarray,
    pick_times_ms: Optional[np.ndarray],
    frequency: float,
    title: str = "Seismic Wiggle Plot",
):
    """
    Creates a simple "wiggle trace" plot for a block of seismic data.

    Args:
        data_block (np.ndarray): The 2D seismic data array to plot
                                 (shape: num_samples, num_traces).
        time_axis_ms (np.ndarray): The 1D time axis in milliseconds.
        pick_times_ms (Optional[np.ndarray]): 1D array of pick times in ms.
                                               NaN values are not plotted.
        title (str): The title for the plot.
    """
    num_samples, num_traces = data_block.shape

    time_axis_ms = (np.arange(num_samples) / frequency) * 1000.0
    sensor_numbers = np.arange(num_traces)

    plt.figure(figsize=(12, 7))
    gain = 0.7 / (np.percentile(np.abs(data_block), 98) + 1e-15)
    for i in sensor_numbers:
        trace_data = data_block[:, i]

        scaled_trace = (trace_data * gain) + i

        plt.plot(scaled_trace, time_axis_ms, "k-", linewidth=0.5)

        # Fill the positive part of the wiggle (like the example image)
        plt.fill_betweenx(
            time_axis_ms,
            i,  # Fill from the trace's "baseline" (its index)
            scaled_trace,  # Fill *to* the wiggle
            where=(scaled_trace > i),  # Only fill where amplitude is positive
            color="black",
            interpolate=True,
        )

    # Plot the first break picks as red dots
    if pick_times_ms is not None:
        plt.plot(
            sensor_numbers, pick_times_ms, "ro", markersize=4, label="First Breaks"
        )
        plt.legend()

    # --- Format the Plot ---
    plt.title(title)
    plt.xlabel("Sensor Number")
    plt.ylabel("Time (ms)")
    plt.xlim(-1, num_traces)  # Add a little padding

    # Set Y-axis to start at 0
    # You can adjust this if you need to see negative time
    min_time = 0
    max_time = np.max(time_axis_ms)

    # Try to zoom in if we have valid picks
    if pick_times_ms is not None and not np.all(np.isnan(pick_times_ms)):
        min_pick_time = np.nanmin(pick_times_ms)
        min_time = max(0, min_pick_time - 5)  # Start 5ms before first pick
        max_time = min(max_time, min_pick_time + 20)  # Show 20ms after first pick

    plt.ylim(min_time, max_time)
    plt.gca().invert_yaxis()  # Put time 0 at the top
    plt.show()
