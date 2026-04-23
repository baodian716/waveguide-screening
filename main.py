"""End-to-end waveguide screening pipeline on synthetic demo data."""

from pathlib import Path

import config
from generate_demo_data import build_dataset
from screening import (
    combine_and,
    mark_divergence_passing,
    mark_overlap_passing,
    mark_peak_top_percent,
    rank_by_efficiency,
)
from visualization import plot_scatter, plot_top_n


def main() -> None:
    print("Generating synthetic dataset...")
    df_er, df_ephi, source_intensity = build_dataset(seed=config.RANDOM_SEED)
    source_total = float(source_intensity.sum())
    print(f"  {len(df_er)} (wavelength, width) combinations")

    print("\nApplying screening conditions...")
    mask_peak = mark_peak_top_percent(df_er, config.PEAK_TOP_PERCENT)
    mask_overlap, overlap_values = mark_overlap_passing(
        df_er, df_ephi, config.OVERLAP_THRESHOLD
    )
    target_idx = config.x_index_for_angle(config.DIVERGENCE_ANGLE_DEG)
    mask_div = mark_divergence_passing(df_er, target_idx)

    print(f"  C1 (peak top {config.PEAK_TOP_PERCENT * 100:.0f}%):       {mask_peak.sum()}")
    print(f"  C2 (overlap >= {config.OVERLAP_THRESHOLD}):    {mask_overlap.sum()}")
    print(f"  C3 (half-div < {config.DIVERGENCE_ANGLE_DEG} deg): {mask_div.sum()}")

    mask_all = combine_and(mask_peak, mask_overlap, mask_div)
    print(f"  All three (AND):              {mask_all.sum()}")

    df_passed = df_er[mask_all].copy()
    df_passed["overlap"] = overlap_values[mask_all]

    if df_passed.empty:
        print("\nNo candidates passed all three conditions. Try a different seed.")
        return

    print("\nRanking by transmission efficiency...")
    df_ranked = rank_by_efficiency(df_passed, source_total)

    n_show = min(config.TOP_N, len(df_ranked))
    print(f"\nTop {n_show} candidates:")
    print(f'{"Rank":>4}  {"Wavelength":>10}  {"Width":>7}  {"Efficiency":>10}  {"Overlap":>8}')
    print("-" * 50)
    for i in range(n_show):
        row = df_ranked.iloc[i]
        print(
            f'{i + 1:>4}  {row["wavelength"]:>10.5f}  {row["width"]:>7.3f}  '
            f'{row["efficiency"]:>10.4f}  {row["overlap"]:>8.4f}'
        )

    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(exist_ok=True)
    plot_scatter(
        df_passed,
        title="Candidates passing all three screening conditions",
        savepath=output_dir / "screening_and.png",
    )
    plot_top_n(
        df_ranked,
        n=config.TOP_N,
        savepath=output_dir / "top10_scatter.png",
    )
    print(f"\nFigures saved to {output_dir}")


if __name__ == "__main__":
    main()
