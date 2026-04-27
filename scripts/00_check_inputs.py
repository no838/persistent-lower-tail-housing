"""Check that the analysis-ready input tables are present and minimally valid."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from utils import data_file, read_csv, require_columns


EXPECTED: dict[str, list[str]] = {
    "universal_pathway_law_city_table_2026-04-20.csv": [
        "persistent_bottom_3plus_share_full_window",
        "ever_bottom_share_full_window",
        "process_persistent_escape_deepen",
        "mean_gini_2018_2022",
    ],
    "community_transition_process_2018_2022.csv": [
        "first_exposure_year",
        "bottom_years_total",
        "persistent_bottom_3plus",
    ],
    "city_transition_process_decomposition_2018_2022.csv": [
        "ever_bottom_count",
        "immediate_escape_share",
        "immediate_repeat_share",
        "deepening_given_repeat",
    ],
    "china_transaction_detail_validation_expansion_city_summary_2026-04-23.csv": [
        "city",
        "never_minus_persistent_rank_gap",
    ],
    "china_transaction_detail_validation_expansion_pair_scores_2026-04-23.csv": [
        "pair_id",
        "city",
        "persistent_match_tier",
        "control_match_tier",
        "both_external_available",
        "persistent_lower_than_control_external",
    ],
    "uk_all_available12_holdout_transfer_summary_2026-04-23.csv": [
        "model",
        "n_splits",
        "mean_holdout_mae",
        "holdout_win_share",
    ],
    "uk_all_available12_holdout_split_table_2026-04-23.csv": [
        "split_id",
        "model",
        "holdout_mae",
    ],
    "uk_top10_holdout_transfer_summary_2026-04-23.csv": [
        "model",
        "n_splits",
        "mean_holdout_mae",
        "holdout_win_share",
    ],
    "france_dvf_department_pathway_smoke_model_summary_2021_2025.csv": [
        "model",
        "pearson",
        "spearman",
        "mean_abs_error",
        "win_share_vs_other",
    ],
    "france_dvf_department_pathway_smoke_city_table_2021_2025.csv": [
        "department",
        "persistent_share_3plus",
        "minimal_law_prediction",
        "exposure_only_prediction",
        "minimal_beats_exposure_only",
    ],
    "component_attribution_board_2026-04-23.csv": [
        "layer",
        "signal",
        "exposure_score",
        "hardening_score",
        "primary_component",
    ],
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path("data/analysis_ready"))
    args = parser.parse_args()

    failures: list[str] = []
    for filename, columns in EXPECTED.items():
        path = data_file(args.data_dir, filename)
        if not path.exists():
            failures.append(f"missing file: {filename}")
            continue
        rows = read_csv(path)
        missing_columns = require_columns(path, rows, columns)
        if missing_columns:
            failures.append(f"{filename}: missing columns {', '.join(missing_columns)}")
        else:
            print(f"OK {filename} ({len(rows)} rows)")

    if failures:
        print("\nInput check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("\nAll expected analysis-ready inputs are present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

