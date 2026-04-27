"""Reproduce the core pathway calibration and exposure-only comparison."""

from __future__ import annotations

import argparse
from pathlib import Path

from utils import data_file, f, fmt, get, mae, pearson, print_rows, read_csv, spearman, write_csv


CITY_TABLE = "universal_pathway_law_city_table_2026-04-20.csv"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path("data/analysis_ready"))
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/tables"))
    args = parser.parse_args()

    rows = read_csv(data_file(args.data_dir, CITY_TABLE))
    observed = [row["persistent_bottom_3plus_share_full_window"] for row in rows]
    pathway = [row["process_persistent_escape_deepen"] for row in rows]
    exposure_only = [row["ever_bottom_share_full_window"] for row in rows]
    gini = [row["mean_gini_2018_2022"] for row in rows]

    metrics = [
        {
            "metric": "pathway_pearson_observed_vs_predicted",
            "value": fmt(pearson(pathway, observed)),
        },
        {
            "metric": "pathway_spearman_observed_vs_predicted",
            "value": fmt(spearman(pathway, observed)),
        },
        {
            "metric": "pathway_mae",
            "value": fmt(mae(pathway, observed)),
        },
        {
            "metric": "exposure_only_pearson_observed_vs_predicted",
            "value": fmt(pearson(exposure_only, observed)),
        },
        {
            "metric": "exposure_only_mae",
            "value": fmt(mae(exposure_only, observed)),
        },
        {
            "metric": "static_gini_pearson_observed_vs_gini",
            "value": fmt(pearson(gini, observed)),
        },
        {
            "metric": "static_gini_spearman_observed_vs_gini",
            "value": fmt(spearman(gini, observed)),
        },
    ]

    residual_rows = []
    for row in rows:
        city = get(row, "city", "城市")
        obs = f(row.get("persistent_bottom_3plus_share_full_window"))
        pred = f(row.get("process_persistent_escape_deepen"))
        exposure = f(row.get("ever_bottom_share_full_window"))
        residual_rows.append(
            {
                "city": city,
                "observed_persistent_share": fmt(obs),
                "pathway_prediction": fmt(pred),
                "pathway_abs_error": fmt(abs(obs - pred) if obs is not None and pred is not None else None),
                "exposure_only_prediction": fmt(exposure),
                "exposure_only_abs_error": fmt(
                    abs(obs - exposure) if obs is not None and exposure is not None else None
                ),
            }
        )

    write_csv(args.out_dir / "pathway_calibration_summary.csv", metrics)
    write_csv(args.out_dir / "pathway_city_residuals.csv", residual_rows)
    print_rows(metrics)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

