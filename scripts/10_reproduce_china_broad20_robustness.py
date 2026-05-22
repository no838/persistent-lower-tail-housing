"""Reproduce broad 20-city China robustness summaries.

This script keeps the broad 20-city frame separate from the canonical 12-city
calibration. The manuscript uses the 12-city frame as the main calibration and
the broader 20-city frame as an internal robustness and timing-sensitivity
check.
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from utils import data_file, f, fmt, get, group_by, mae, pearson, print_rows, read_csv, spearman, write_csv


BROAD20_TABLE = "broad20_city_pathway_law_table_2018_2022.csv"
BROAD20_MODEL_SUMMARY = "china_internal_holdout_replication_broad20_model_summary_2026-04-21.csv"
BROAD20_SPLIT_TABLE = "china_internal_holdout_replication_broad20_split_table_2026-04-21.csv"
BROAD20_TRANSFER_SUMMARY = "china_internal_holdout_replication_broad20_transfer_summary_2026-04-21.csv"


def split_winners(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    winners: list[dict[str, object]] = []
    for split_id, split_rows in group_by(rows, "split_id").items():
        scored = [(row.get("model", ""), f(row.get("holdout_mae"))) for row in split_rows]
        scored = [(model, value) for model, value in scored if value is not None]
        if not scored:
            continue
        winner, value = min(scored, key=lambda item: item[1])
        winners.append({"split_id": split_id, "winner": winner, "winning_holdout_mae": fmt(value)})
    return winners


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path("data/analysis_ready"))
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/tables"))
    args = parser.parse_args()

    rows = read_csv(data_file(args.data_dir, BROAD20_TABLE))
    observed = [row["persistent_bottom_3plus_share_full_window"] for row in rows]
    pathway = [row["pred_minimal_law"] for row in rows]
    exposure_only = [row["pred_exposure_only"] for row in rows]
    timing = [row["pred_timing_extension"] for row in rows]
    gini = [row["mean_gini_2018_2022"] for row in rows]

    metrics = [
        {"metric": "broad20_n_cities", "value": str(len(rows))},
        {"metric": "broad20_pathway_pearson_observed_vs_predicted", "value": fmt(pearson(pathway, observed))},
        {"metric": "broad20_pathway_spearman_observed_vs_predicted", "value": fmt(spearman(pathway, observed))},
        {"metric": "broad20_pathway_mae", "value": fmt(mae(pathway, observed))},
        {"metric": "broad20_timing_extension_mae", "value": fmt(mae(timing, observed))},
        {"metric": "broad20_exposure_only_mae", "value": fmt(mae(exposure_only, observed))},
        {"metric": "broad20_static_gini_pearson_observed_vs_gini", "value": fmt(pearson(gini, observed))},
    ]

    residual_rows = []
    for row in rows:
        city = get(row, "city", "城市")
        obs = f(row.get("persistent_bottom_3plus_share_full_window"))
        pred = f(row.get("pred_minimal_law"))
        exposure = f(row.get("pred_exposure_only"))
        timing_pred = f(row.get("pred_timing_extension"))
        residual_rows.append(
            {
                "city": city,
                "observed_persistent_share": fmt(obs),
                "pathway_prediction": fmt(pred),
                "pathway_abs_error": fmt(abs(obs - pred) if obs is not None and pred is not None else None),
                "timing_extension_prediction": fmt(timing_pred),
                "timing_extension_abs_error": fmt(
                    abs(obs - timing_pred) if obs is not None and timing_pred is not None else None
                ),
                "exposure_only_prediction": fmt(exposure),
                "exposure_only_abs_error": fmt(
                    abs(obs - exposure) if obs is not None and exposure is not None else None
                ),
            }
        )

    model_summary = read_csv(data_file(args.data_dir, BROAD20_MODEL_SUMMARY))
    split_rows = read_csv(data_file(args.data_dir, BROAD20_SPLIT_TABLE))
    transfer_summary = read_csv(data_file(args.data_dir, BROAD20_TRANSFER_SUMMARY))
    winners = split_winners(split_rows)
    counts = Counter(row["winner"] for row in winners)
    n = len(winners)
    winner_summary = [
        {
            "model": model,
            "split_win_count": counts.get(model, 0),
            "split_win_share": fmt(counts.get(model, 0) / n if n else None),
        }
        for model in sorted({row.get("model", "") for row in split_rows})
    ]

    write_csv(args.out_dir / "china_broad20_pathway_calibration_summary.csv", metrics)
    write_csv(args.out_dir / "china_broad20_pathway_city_residuals.csv", residual_rows)
    write_csv(args.out_dir / "china_broad20_holdout_model_summary.csv", model_summary)
    write_csv(args.out_dir / "china_broad20_holdout_transfer_summary.csv", transfer_summary)
    write_csv(args.out_dir / "china_broad20_holdout_split_winners.csv", winners)
    write_csv(args.out_dir / "china_broad20_holdout_winner_summary_from_splits.csv", winner_summary)
    print_rows(metrics)
    print_rows(winner_summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
