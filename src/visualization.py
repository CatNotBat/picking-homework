import numpy as np
import matplotlib.pyplot as plt
from typing import Optional


def plot_wiggles(
    data_block: np.ndarray,
    pick_times_ms: Optional[np.ndarray],
    frequency: float,
    title: str = "Seismic Wiggle Plot",
):
    num_samples, num_traces = data_block.shape

    time_axis_ms = (np.arange(num_samples) / frequency) * 1000.0
    sensor_numbers = np.arange(num_traces)

    plt.figure(figsize=(12, 7))
    gain = 0.7 / (np.percentile(np.abs(data_block), 98) + 1e-15)
    for i in sensor_numbers:
        trace_data = data_block[:, i]

        scaled_trace = (trace_data * gain) + i

        plt.plot(scaled_trace, time_axis_ms, "k-", linewidth=0.5)

    if pick_times_ms is not None:
        plt.plot(
            sensor_numbers, pick_times_ms, "ro", markersize=4, label="First Breaks"
        )
        plt.legend()

    plt.title(title)
    plt.xlabel("Sensor Number")
    plt.ylabel("Time (ms)")

    min_time = 0
    max_time = np.max(time_axis_ms)

    # Try to zoom in if we have valid picks
    if pick_times_ms is not None and not np.all(np.isnan(pick_times_ms)):
        min_pick_time = np.nanmin(pick_times_ms)
        min_time = max(0, min_pick_time - 5)
        max_time = min(max_time, min_pick_time + 30)

    plt.ylim(min_time, max_time)
    plt.gca().invert_yaxis()  # Put time 0 at the top
    plt.show()
