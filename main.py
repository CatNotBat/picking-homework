from picker import SeismicPicker
from strategies.absolute_threshold import AbsoluteThresholdStrategy
from data_loader import load_seismic_data
from analysis import convert_indices_to_time
from visualization import plot_wiggles

# --- Configuration ---
ABSOLUTE_THRESHOLD = 1e-9
BLOCK_SIZE = 64
SAMPLING_FREQUENCY = 2000.0

if __name__ == "__main__":
    # 1. Load data
    print("Loading data...")
    seismic_data, _, _ = load_seismic_data("data/simulation_ricker.mat")
    strategy = AbsoluteThresholdStrategy(threshold=ABSOLUTE_THRESHOLD)
    picker = SeismicPicker(strategy=strategy, sampling_frequency=SAMPLING_FREQUENCY)

    all_breaks_indices = picker.run_picking(seismic_data)
    all_breaks_times_ms = convert_indices_to_time(
        all_breaks_indices, SAMPLING_FREQUENCY
    )
    plot_wiggles(seismic_data, all_breaks_times_ms, SAMPLING_FREQUENCY)
