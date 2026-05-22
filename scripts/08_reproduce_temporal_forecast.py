"""Reproduce v13 temporal anti-identity forecast summaries."""

from __future__ import annotations

import argparse
from pathlib import Path

from utils import data_file, f, fmt, read_csv, write_csv


EARLY_PERFORMANCE = "china_early_window_forecast_performance_v13_2026-05-14.csv"
ROLLING_PERFORMANCE = "china_rolling_origin_forecast_performance_v13_2026-05-14.csv"
PERMUTATION_NULL = "china_early_window_forecast_permutation_null_v13_2026-05-14.csv"


def row_for(rows: list[dict[str, str]], cutoff_q: float, predictor: str) -> dict[str, str]:
    for row in rows:
        q = f(row.get("cutoff_q"))
        if q is not None and abs(q - cutoff_q) < 1e-9 and row.get("predictor") == predictor:
            return row
    raise ValueError(f"missing predictor={predictor} cutoff_q={cutoff_q}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path("data/analysis_ready"))
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/tables"))
    args = parser.parse_args()

    early = read_csv(data_file(args.data_dir, EARLY_PERFORMANCE))
    rolling = read_csv(data_file(args.data_dir, ROLLING_PERFORMANCE))
    permutation = read_csv(data_file(args.data_dir, PERMUTATION_NULL))

    early_pathway = row_for(early, 0.10, "pathway_active")
    early_exposure = row_for(early, 0.10, "exposure_only")
    early_markov = row_for(early, 0.10, "markov_pair")
    early_independence = row_for(early, 0.10, "independence")

    rolling_pathway = row_for(rolling, 0.10, "pathway_active")
    rolling_exposure = row_for(rolling, 0.10, "exposure_only")
    rolling_markov = row_for(rolling, 0.10, "markov_pair")
    rolling_independence = row_for(rolling, 0.10, "independence")

    null_maes = [f(row.get("mae")) for row in permutation]
    null_maes = sorted(value for value in null_maes if value is not None)
    null_median = null_maes[len(null_maes) // 2] if null_maes else None
    early_pathway_mae = f(early_pathway.get("mae"))
    null_percentile = None
    if null_maes and early_pathway_mae is not None:
        null_percentile = sum(value <= early_pathway_mae for value in null_maes) / len(null_maes)

    rows = [
        {
            "test": "single_split_2018_2020_to_2021_2022",
            "cutoff_q": "0.10",
            "pathway_mae": early_pathway.get("mae"),
            "exposure_only_mae": early_exposure.get("mae"),
            "independence_mae": early_independence.get("mae"),
            "markov_pair_mae": early_markov.get("mae"),
            "pathway_pearson": early_pathway.get("pearson"),
            "pathway_mae_ci_low": early_pathway.get("mae_ci_low"),
            "pathway_mae_ci_high": early_pathway.get("mae_ci_high"),
            "sequence_permutation_null_median_mae": fmt(null_median),
            "observed_pathway_mae_percentile_in_null": fmt(null_percentile),
        },
        {
            "test": "rolling_origin_2010_2022",
            "cutoff_q": "0.10",
            "pathway_mae": rolling_pathway.get("mae"),
            "exposure_only_mae": rolling_exposure.get("mae"),
            "independence_mae": rolling_independence.get("mae"),
            "markov_pair_mae": rolling_markov.get("mae"),
            "pathway_pearson": rolling_pathway.get("pearson"),
            "pathway_mae_ci_low": rolling_pathway.get("mae_ci_low"),
            "pathway_mae_ci_high": rolling_pathway.get("mae_ci_high"),
            "sequence_permutation_null_median_mae": "NA",
            "observed_pathway_mae_percentile_in_null": "NA",
        },
    ]

    write_csv(args.out_dir / "temporal_forecast_anti_identity_summary_v13.csv", rows)
    for row in rows:
        print(", ".join(f"{key}={value}" for key, value in row.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
