import numpy as np
from picker import SeismicPicker
from strategies import sta_lta
from data_loader import load_seismic_data
from noise_generator import generate_white_noise_to_get_target_snr
import matplotlib.pyplot as plt

SNR_LEVELS_TO_CHECK = [50, 20, 10, 5, 2, 1, 0.5]
TRIGGER_RATIO = 3.2
SAMPLING_FREQUENCY = 2000.0
SNR = 10
FILE_PATH = "data/simulation_continuous.mat"

if __name__ == "__main__":
    # 1. Load data
    print("Loading data...")
    seismic_data, fs, geometry = load_seismic_data(FILE_PATH)
    strategy = sta_lta.ModelDrivenSTALTAStrategy(
        short_window=120, long_window=400, ratio_threshold=TRIGGER_RATIO
    )

    picker = SeismicPicker(strategy=strategy, sampling_frequency=SAMPLING_FREQUENCY)

    ground_truth_picks = picker.run_picking(seismic_data, geometry)

    all_errors = []

    for snr in SNR_LEVELS_TO_CHECK:
        strategy = sta_lta.ModelDrivenSTALTAStrategy(
            short_window=100, long_window=600, ratio_threshold=1.6
        )
        picker = SeismicPicker(strategy=strategy, sampling_frequency=SAMPLING_FREQUENCY)
        noisey_data = seismic_data + generate_white_noise_to_get_target_snr(
            seismic_data, snr
        )
        noisy_picks = picker.run_picking(noisey_data, geometry)
        pick_errors_in_samples = noisy_picks - ground_truth_picks
        squared_errors = pick_errors_in_samples**2
        mean_squared_error = np.nanmean(squared_errors)
        rmse_in_samples = np.sqrt(mean_squared_error)
        all_errors.append(rmse_in_samples)

    plt.plot(SNR_LEVELS_TO_CHECK, all_errors, "o-")

    plt.xlabel("Signal-to-Noise Ratio (SNR)")

    plt.ylabel("Error (RMSE in samples)")

    plt.title("Algorithm Robustness to White Noise")

    plt.show()
