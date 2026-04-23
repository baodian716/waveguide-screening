"""Synthetic field data generator.

Produces |E_r|^2 and |E_phi|^2 distributions across (width, wavelength, x).
The synthesis is physics-inspired (Gaussian envelope + radial ringing) with a
"sweet spot" in parameter space that naturally passes all three screening
conditions, so the downstream pipeline has meaningful candidates to rank.

NOTE: This is demo data, not real simulation output.
"""

import numpy as np
import pandas as pd

from config import WIDTHS, WAVELENGTHS, X_POSITIONS


# Sweet spot in (width, wavelength) — combinations near here will tend to pass
# all three screening conditions in the downstream pipeline.
_SWEET_WIDTH = 0.5
_SWEET_WAVELENGTH = 1.0


def build_dataset(seed: int = 42):
    """Generate the full synthetic dataset.

    Returns:
        df_er:           DataFrame with columns [wavelength, width, x_0, ..., x_N]
        df_ephi:         DataFrame with the same shape, slightly perturbed from Er
        source_intensity: 1D ndarray, source-plane |E|^2 sampled at X_POSITIONS
    """
    rng = np.random.default_rng(seed)

    # Broadcast grids: shape (n_w, n_l, n_x)
    W = WIDTHS[:, None, None]
    L = WAVELENGTHS[None, :, None]
    X = X_POSITIONS[None, None, :]

    # Distance from sweet spot in normalized (width, wavelength) space.
    delta = np.hypot((W - _SWEET_WIDTH) / 0.4, (L - _SWEET_WAVELENGTH) / 0.5)

    # Beam tightness: tight near sweet spot, broad far away.
    sigma = 1.5 + 8.0 * delta + rng.normal(0, 0.3, size=delta.shape)
    sigma = np.maximum(sigma, 0.5)

    # Peak amplitude: high near sweet spot, low far away.
    peak_amp = np.exp(-(delta ** 2)) * (1.0 + rng.normal(0, 0.05, size=delta.shape))
    peak_amp = np.maximum(peak_amp, 1e-6)

    # Gaussian envelope along r, with mild radial ringing keyed to wavelength.
    k = 2 * np.pi / np.maximum(L, 0.1)
    envelope = np.exp(-(X ** 2) / (2 * sigma ** 2))
    rings = 1.0 + 0.1 * np.cos(k * X)

    er_amp = peak_amp * envelope * rings
    er_energy = er_amp ** 2

    # Tiny additive noise so two combinations are never exactly equal.
    er_energy = er_energy + rng.normal(0, 1e-3 * peak_amp ** 2, size=er_energy.shape)
    er_energy = np.clip(er_energy, 0.0, None)

    # Ephi mirrors Er with a small multiplicative perturbation. About 30% of
    # combinations get an additional larger perturbation that breaks overlap.
    perturbation = 1.0 + rng.normal(0, 0.05, size=er_energy.shape)
    break_mask = rng.random(size=(WIDTHS.size, WAVELENGTHS.size, 1)) < 0.3
    perturbation = perturbation + rng.normal(0, 0.18, size=er_energy.shape) * break_mask
    ephi_energy = np.clip(er_energy * perturbation, 0.0, None)

    # Reshape to (n_combinations, n_x) and attach (wavelength, width) labels.
    n_x = X_POSITIONS.size
    er_flat = er_energy.reshape(-1, n_x)
    ephi_flat = ephi_energy.reshape(-1, n_x)

    wlen_grid, w_grid = np.meshgrid(WAVELENGTHS, WIDTHS)
    labels = np.column_stack([wlen_grid.ravel(), w_grid.ravel()])

    cols = ["wavelength", "width"] + [f"x_{i}" for i in range(n_x)]
    df_er = pd.DataFrame(np.column_stack([labels, er_flat]), columns=cols)
    df_ephi = pd.DataFrame(np.column_stack([labels, ephi_flat]), columns=cols)

    # Source plane: a tight Gaussian centered on r=0. The amplitude is scaled
    # so that the top demo candidates land in the 5-25% efficiency range,
    # roughly matching the order of magnitude reported in the original study.
    source_intensity = 10.0 * np.exp(-(X_POSITIONS / 3.0) ** 2)

    return df_er, df_ephi, source_intensity
