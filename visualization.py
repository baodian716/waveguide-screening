"""Two scatter plots: AND-passed candidates and Top-N candidates."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from config import WIDTHS, WAVELENGTHS


def _style_axes(ax, title: str) -> None:
    ax.set_xlabel("Width (a)")
    ax.set_ylabel("Wavelength (a)")
    ax.set_title(title)
    ax.set_xlim(WIDTHS.min() - 0.02, WIDTHS.max() + 0.02)
    ax.set_ylim(WAVELENGTHS.min() - 0.02, WAVELENGTHS.max() + 0.02)
    ax.grid(True, alpha=0.3)


def plot_scatter(df: pd.DataFrame, title: str, savepath: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.plot(df["width"], df["wavelength"], "bx", markersize=6)
    _style_axes(ax, title)
    fig.tight_layout()
    fig.savefig(savepath, dpi=150)
    plt.close(fig)


def plot_top_n(df_ranked: pd.DataFrame, n: int, savepath: Path) -> None:
    top = df_ranked.head(n)
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.plot(top["width"], top["wavelength"], "bx", markersize=12, mew=2)
    eff_min, eff_max = top["efficiency"].min(), top["efficiency"].max()
    _style_axes(
        ax,
        f"Top {len(top)} candidates  (efficiency {eff_min:.3f} ~ {eff_max:.3f})",
    )
    fig.tight_layout()
    fig.savefig(savepath, dpi=150)
    plt.close(fig)
