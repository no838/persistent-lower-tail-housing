"""Build lightweight diagnostic figures from the released analysis-ready tables.

These are reproducibility diagnostics, not the full designed manuscript figure
layout. They allow readers to inspect the same core relationships used by the
publication figures.
"""

from __future__ import annotations

import argparse
import os
import tempfile
from pathlib import Path

from utils import data_file, f, get, group_by, read_csv, truthy


CITY_TABLE = "universal_pathway_law_city_table_2026-04-20.csv"
PAIR_SCORES = "china_transaction_detail_validation_expansion_pair_scores_2026-04-23.csv"
UK_SPLITS = "uk_all_available12_holdout_split_table_2026-04-23.csv"
UK_CITYFRAME_PERFORMANCE = "uk_cityframe_performance_summary_2018_2022.csv"
FRANCE_TABLE = "france_dvf_department_pathway_smoke_city_table_2021_2025.csv"


def import_pyplot():
    cache_dir = Path(tempfile.gettempdir()) / "persistent_lower_tail_matplotlib_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(cache_dir))
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise SystemExit(
            "matplotlib is required for diagnostic figures. "
            "Install it with `pip install -r requirements.txt`."
        ) from exc
    return plt


def pathway_calibration(data_dir: Path, fig_dir: Path) -> None:
    plt = import_pyplot()
    rows = read_csv(data_file(data_dir, CITY_TABLE))
    observed = [f(row["persistent_bottom_3plus_share_full_window"]) for row in rows]
    predicted = [f(row["process_persistent_escape_deepen"]) for row in rows]
    observed = [value for value in observed if value is not None]
    predicted = [value for value in predicted if value is not None]
    limit = max(observed + predicted) * 1.08

    fig, ax = plt.subplots(figsize=(5.2, 5.2))
    ax.scatter(predicted, observed, s=36, color="#5F7FA3", alpha=0.85, edgecolor="white")
    ax.plot([0, limit], [0, limit], color="#8C8C8C", lw=1.0, ls="--")
    ax.set_xlim(0, limit)
    ax.set_ylim(0, limit)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("Predicted persistent share")
    ax.set_ylabel("Observed persistent share")
    ax.set_title("Pathway calibration")
    ax.grid(color="#D9D9D9", lw=0.5, alpha=0.35)
    fig.tight_layout()
    fig.savefig(fig_dir / "diagnostic_pathway_calibration.png", dpi=300)
    plt.close(fig)


def transaction_pairs(data_dir: Path, fig_dir: Path) -> None:
    plt = import_pyplot()
    rows = [row for row in read_csv(data_file(data_dir, PAIR_SCORES)) if truthy(row.get("both_external_available"))]

    fig, ax = plt.subplots(figsize=(5.8, 4.0))
    for row in rows:
        y0 = f(row.get("persistent_tx_price_2018_2022"))
        y1 = f(row.get("control_tx_price_2018_2022"))
        if y0 is None or y1 is None:
            continue
        ax.plot([0, 1], [y0, y1], color="#6F9A83", alpha=0.25, lw=1.1)
        ax.scatter([0], [y0], color="#C86C63", s=18, alpha=0.55, zorder=3)
        ax.scatter([1], [y1], color="#5E8E76", s=18, alpha=0.55, zorder=3)
    ax.set_xticks([0, 1], ["Persistent-bottom", "Matched control"])
    ax.set_ylabel("Transaction price")
    ax.set_title("China transaction-pair validation")
    ax.grid(axis="y", color="#D9D9D9", lw=0.5, alpha=0.35)
    fig.tight_layout()
    fig.savefig(fig_dir / "diagnostic_china_transaction_pairs.png", dpi=300)
    plt.close(fig)


def uk_holdout_distribution(data_dir: Path, fig_dir: Path) -> None:
    plt = import_pyplot()
    rows = read_csv(data_file(data_dir, UK_SPLITS))
    groups = group_by(rows, "model")
    order = ["minimal_law", "timing_extension", "exposure_only"]
    values = [[f(row.get("holdout_mae")) for row in groups.get(model, [])] for model in order]
    values = [[value for value in model_values if value is not None] for model_values in values]

    fig, ax = plt.subplots(figsize=(5.8, 4.0))
    bp = ax.boxplot(values, patch_artist=True, widths=0.45, showfliers=False)
    colors = ["#4F7E9F", "#D9A15B", "#B8B8B8"]
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.28)
        patch.set_edgecolor(color)
    for i, model_values in enumerate(values, start=1):
        ax.scatter([i] * len(model_values), model_values, s=7, alpha=0.12, color=colors[i - 1])
    ax.set_xticks([1, 2, 3], ["Minimal law", "Timing", "Exposure-only"])
    ax.set_ylabel("Holdout MAE")
    ax.set_title("UK holdout distribution")
    ax.grid(axis="y", color="#D9D9D9", lw=0.5, alpha=0.35)
    fig.tight_layout()
    fig.savefig(fig_dir / "diagnostic_uk_holdout_distribution.png", dpi=300)
    plt.close(fig)


def uk_cityframe_performance(data_dir: Path, fig_dir: Path) -> None:
    plt = import_pyplot()
    path = data_file(data_dir, UK_CITYFRAME_PERFORMANCE)
    if not path.exists():
        return
    rows = read_csv(path)
    rows = [row for row in rows if row.get("cohort_type") == "available"]
    order = ["ttwa", "lad", "bua"]
    rows_by_frame = {row.get("frame_type", ""): row for row in rows}
    pathway = [f(rows_by_frame.get(frame, {}).get("mae_pathway")) for frame in order]
    exposure = [f(rows_by_frame.get(frame, {}).get("mae_exposure_only")) for frame in order]
    if any(value is None for value in pathway + exposure):
        return

    fig, ax = plt.subplots(figsize=(5.8, 4.0))
    x = list(range(len(order)))
    width = 0.34
    ax.bar([i - width / 2 for i in x], pathway, width, color="#4F7E9F", alpha=0.82, label="Pathway")
    ax.bar([i + width / 2 for i in x], exposure, width, color="#B8B8B8", alpha=0.75, label="Exposure-only")
    ax.set_xticks(x, ["TTWA", "LAD", "BUA"])
    ax.set_ylabel("Mean absolute error")
    ax.set_title("UK ONSPD-linked city-frame performance")
    ax.legend(frameon=False)
    ax.grid(axis="y", color="#D9D9D9", lw=0.5, alpha=0.35)
    fig.tight_layout()
    fig.savefig(fig_dir / "diagnostic_uk_cityframe_performance.png", dpi=300)
    plt.close(fig)


def france_calibration(data_dir: Path, fig_dir: Path) -> None:
    plt = import_pyplot()
    rows = read_csv(data_file(data_dir, FRANCE_TABLE))
    observed = [f(row["persistent_share_3plus"]) for row in rows]
    predicted = [f(row["minimal_law_prediction"]) for row in rows]
    observed = [value for value in observed if value is not None]
    predicted = [value for value in predicted if value is not None]
    limit = max(observed + predicted) * 1.08

    fig, ax = plt.subplots(figsize=(5.2, 5.2))
    ax.scatter(predicted, observed, s=24, color="#7DA493", alpha=0.75, edgecolor="white")
    ax.plot([0, limit], [0, limit], color="#8C8C8C", lw=1.0, ls="--")
    ax.set_xlim(0, limit)
    ax.set_ylim(0, limit)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("Predicted persistent share")
    ax.set_ylabel("Observed persistent share")
    ax.set_title("France department-frame extension")
    ax.grid(color="#D9D9D9", lw=0.5, alpha=0.35)
    fig.tight_layout()
    fig.savefig(fig_dir / "diagnostic_france_extension_calibration.png", dpi=300)
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path("data/analysis_ready"))
    parser.add_argument("--fig-dir", type=Path, default=Path("outputs/figures"))
    args = parser.parse_args()
    args.fig_dir.mkdir(parents=True, exist_ok=True)

    pathway_calibration(args.data_dir, args.fig_dir)
    transaction_pairs(args.data_dir, args.fig_dir)
    uk_holdout_distribution(args.data_dir, args.fig_dir)
    uk_cityframe_performance(args.data_dir, args.fig_dir)
    france_calibration(args.data_dir, args.fig_dir)
    print(f"Wrote diagnostic figures to {args.fig_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
