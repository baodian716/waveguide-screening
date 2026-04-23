"""Constants for the waveguide screening pipeline."""

import numpy as np

# Parameter grids
WIDTHS = np.arange(0.1, 0.92, 0.02)              # 41 widths
WAVELENGTHS = np.linspace(0.714, 1.666, 200)     # 200 wavelengths
X_POSITIONS = np.linspace(0.0, 39.5, 80)         # 80 detector positions along r

# Physics parameter
PROPAGATION_DISTANCE = 200.0   # detector plane sits at z = 200a in the original study

# Screening thresholds
PEAK_TOP_PERCENT = 0.05          # condition 1: keep top 5% by center peak
OVERLAP_THRESHOLD = 0.95         # condition 2: Er/Ephi overlap integral >= 0.95
DIVERGENCE_ANGLE_DEG = 1.5       # condition 3: half-divergence angle threshold

# Output
TOP_N = 10
RANDOM_SEED = 42


def x_index_for_angle(angle_deg: float) -> int:
    """Return the x_positions index closest to the radius matching `angle_deg`
    at z = PROPAGATION_DISTANCE. Replaces the MATLAB hard-coded column 18.
    """
    target_radius = PROPAGATION_DISTANCE * np.tan(np.deg2rad(angle_deg))
    return int(np.argmin(np.abs(X_POSITIONS - target_radius)))
