"""Physics metrics used by the screening pipeline.

All functions are pure and operate on 1D ndarrays representing |E|^2 sampled
along the radial detector axis.
"""

import numpy as np


def peak_intensity(field_row: np.ndarray) -> float:
    """Center-axis (r=0) intensity."""
    return float(field_row[0])


def overlap_integral(er: np.ndarray, ephi: np.ndarray) -> float:
    """Normalized overlap eta = (sum Er*Ephi)^2 / (sum Er^2 * sum Ephi^2)."""
    numerator = float(np.sum(er * ephi)) ** 2
    denominator = float(np.sum(er ** 2)) * float(np.sum(ephi ** 2))
    return numerator / denominator if denominator > 0 else 0.0


def divergence_ok(field_row: np.ndarray, target_idx: int) -> bool:
    """True when the intensity at `target_idx` has dropped below 1/e^2 of center,
    i.e. the half-divergence angle is within the configured threshold."""
    return bool(field_row[target_idx] < field_row[0] / np.e ** 2)


def transmission_efficiency(field_row: np.ndarray, source_total: float) -> float:
    """Detector-plane total energy normalized by source-plane total energy."""
    return float(np.sum(field_row) / source_total)
