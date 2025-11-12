from picker import SeismicPicker
from strategies import sta_lta
from data_loader import load_seismic_data
from analysis import convert_indices_to_time
from visualization import plot_sismograma


ABSOLUTE_THRESHOLD = 2e-5
TRIGGER_RATIO = 3.2
BLOCK_SIZE = 64
SAMPLING_FREQUENCY = 2000.0
FILE_PATH = "data/simulation_continuous.mat"

if __name__ == "__main__":
    seismic_data, fs, geometry = load_seismic_data(FILE_PATH)
    strategy = sta_lta.ModelDrivenSTALTAStrategy(
        short_window=120, long_window=400, ratio_threshold=TRIGGER_RATIO
    )
    picker = SeismicPicker(strategy=strategy, sampling_frequency=SAMPLING_FREQUENCY)

    all_breaks_indices = picker.run_picking(seismic_data, geometry)
    all_breaks_times_ms = convert_indices_to_time(
        all_breaks_indices, SAMPLING_FREQUENCY
    )

    print(all_breaks_indices)
    plot_sismograma(seismic_data, all_breaks_times_ms, SAMPLING_FREQUENCY)
