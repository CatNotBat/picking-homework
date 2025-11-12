import numpy as np


def generate_white_noise_to_get_target_snr(
    data: np.ndarray, target_snr: float
) -> np.ndarray:
    peak_signal = np.max(np.abs(data))
    target_noise_peak = peak_signal / target_snr

    white_noise = np.random.normal(0, 1, size=data.shape)
    scaled_noise = _scale_noise_to_target_pick(white_noise, target_noise_peak)

    return scaled_noise


def generate_pink_noise_to_get_target_snr(
    data: np.ndarray, target_snr: float, fs: float
) -> np.ndarray:
    white_noise = np.random.normal(0, 1, size=data.shape)
    white_fft = np.fft.rfft(white_noise, axis=0)
    frequencies = np.fft.rfftfreq(data.shape[0], d=1 / fs)
    pink_filter = 1.0 / np.sqrt(frequencies + 1e-15)
    pink_fft = white_fft * pink_filter[:, np.newaxis]
    pink_noise = np.fft.irfft(pink_fft, n=data.shape[0], axis=0)

    peak_signal = np.max(np.abs(data))
    target_noise_peak = peak_signal / target_snr

    scaled_noise = _scale_noise_to_target_pick(pink_noise, target_noise_peak)

    return scaled_noise


def _scale_noise_to_target_pick(noise: np.ndarray, target_pick: float) -> np.ndarray:
    current_noise_peak = np.max(np.abs(noise))
    scaling_factor = target_pick / current_noise_peak
    scaled_noise = noise * scaling_factor

    return scaled_noise
