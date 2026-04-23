"""Apply screening conditions and rank surviving candidates.

Operates on the DataFrames produced by `generate_demo_data.build_dataset`,
where each row is one (wavelength, width) combination and the x_* columns
hold |E|^2 along the radial axis.
"""

import numpy as np
import pandas as pd

_X_PREFIX = "x_"


def _x_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if c.startswith(_X_PREFIX)]


def mark_peak_top_percent(df_er: pd.DataFrame, top_pct: float) -> pd.Series:
    """Condition 1: keep rows whose center-axis intensity falls in the top fraction."""
    threshold = df_er["x_0"].quantile(1 - top_pct)
    return df_er["x_0"] >= threshold


def mark_overlap_passing(
    df_er: pd.DataFrame, df_ephi: pd.DataFrame, threshold: float
) -> tuple[pd.Series, pd.Series]:
    """Condition 2: vectorized overlap integral per row.

    Returns (boolean mask, overlap values) so callers can both filter and report.
    """
    x_cols = _x_columns(df_er)
    er = df_er[x_cols].to_numpy()
    ephi = df_ephi[x_cols].to_numpy()

    numerator = (er * ephi).sum(axis=1) ** 2
    denominator = (er ** 2).sum(axis=1) * (ephi ** 2).sum(axis=1)
    overlap = np.where(denominator > 0, numerator / denominator, 0.0)

    overlap_series = pd.Series(overlap, index=df_er.index, name="overlap")
    mask = overlap_series >= threshold
    return mask, overlap_series


def mark_divergence_passing(df_er: pd.DataFrame, target_idx: int) -> pd.Series:
    """Condition 3: intensity at the target radius < 1/e^2 of the center."""
    target_col = _x_columns(df_er)[target_idx]
    return df_er[target_col] < df_er["x_0"] / np.e ** 2


def combine_and(*masks: pd.Series) -> pd.Series:
    """Logical AND across an arbitrary number of boolean masks."""
    result = masks[0].copy()
    for m in masks[1:]:
        result &= m
    return result


def rank_by_efficiency(df_filtered: pd.DataFrame, source_total: float) -> pd.DataFrame:
    """Add an `efficiency` column and sort by it descending."""
    x_cols = _x_columns(df_filtered)
    eff = df_filtered[x_cols].sum(axis=1) / source_total
    out = df_filtered.copy()
    out["efficiency"] = eff
    return out.sort_values("efficiency", ascending=False).reset_index(drop=True)
