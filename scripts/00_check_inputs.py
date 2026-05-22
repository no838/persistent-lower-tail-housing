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
    "broad20_city_pathway_law_table_2018_2022.csv": [
        "persistent_bottom_3plus_share_full_window",
        "ever_bottom_share_full_window",
        "pred_minimal_law",
        "pred_exposure_only",
        "pred_timing_extension",
    ],
    "china_internal_holdout_replication_broad20_model_summary_2026-04-21.csv": [
        "model",
        "n_splits",
        "mean_holdout_mae",
        "holdout_win_share",
    ],
    "china_internal_holdout_replication_broad20_split_table_2026-04-21.csv": [
        "split_id",
        "model",
        "holdout_mae",
        "holdout_winner",
    ],
    "china_internal_holdout_replication_broad20_transfer_summary_2026-04-21.csv": [
        "n_cities",
        "holdout_size",
        "n_splits",
        "holdout_minimal_win_share",
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
    "uk_cityframe_performance_summary_2018_2022.csv": [
        "country",
        "frame_type",
        "cohort_type",
        "n_frames",
        "mae_pathway",
        "mae_exposure_only",
        "relative_mae_reduction",
    ],
    "uk_cityframe_pathway_metrics_2018_2022.csv": [
        "country",
        "frame_type",
        "frame_id",
        "cohort_type",
        "X_exposure",
        "lambda_immediate_escape",
        "delta_repeat_deepening",
        "P_observed",
        "P_predicted_pathway",
        "P_predicted_exposure_only",
    ],
    "uk_cityframe_panel_coverage_2018_2022.csv": [
        "frame_type",
        "n_frames",
        "n_units",
        "unit_year_rows",
        "start_year",
        "end_year",
        "total_transactions",
    ],
    "uk_old_vs_cityframe_performance_comparison_2018_2022.csv": [
        "country",
        "validation_version",
        "frame_type",
        "cohort_type",
        "mae_pathway",
        "mae_exposure_only",
        "relative_mae_reduction",
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
    "china_early_window_forecast_performance_v13_2026-05-14.csv": [
        "cutoff_q",
        "predictor",
        "target",
        "pearson",
        "mae",
        "mae_ci_low",
        "mae_ci_high",
    ],
    "china_early_window_forecast_permutation_null_v13_2026-05-14.csv": [
        "cutoff_q",
        "permutation_id",
        "null_type",
        "mae",
        "observed_pathway_active_mae",
    ],
    "china_rolling_origin_forecast_performance_v13_2026-05-14.csv": [
        "cutoff_q",
        "predictor",
        "n_windows",
        "pearson",
        "mae",
        "mae_ci_low",
        "mae_ci_high",
    ],
    "pathway_components_uncertainty_v13_1_2026-05-14.csv": [
        "test",
        "cutoff_q",
        "component",
        "mean_unweighted",
        "bootstrap_mean_ci_low",
        "bootstrap_mean_ci_high",
    ],
    "pathway_forecast_city_jackknife_v13_1_2026-05-14.csv": [
        "test",
        "cutoff_q",
        "left_out_city",
        "pathway_mae",
        "exposure_only_mae",
        "markov_pair_mae",
        "pathway_beats_exposure_only",
        "markov_beats_pathway",
    ],
    "threshold_policy_and_sensitivity_v13_1_2026-05-14.csv": [
        "test",
        "cutoff_q",
        "threshold_role",
        "predictor",
        "mae",
        "mae_ci_low",
        "mae_ci_high",
    ],
    "pathway_law_horizon_sweep_v13_4_2026-05-14_performance.csv": [
        "cutoff_q",
        "horizon_years",
        "target_mode",
        "predictor",
        "mae",
        "mae_minus_markov_stationary",
    ],
    "pathway_law_horizon_sweep_v13_4_2026-05-14_collapse.csv": [
        "cutoff_q",
        "horizon_years",
        "target_mode",
        "kernel_vs_target_after_exposure_pearson",
        "kernel_vs_target_after_exposure_mae",
    ],
    "pathway_law_evidence_matrix_v13_4_2026-05-14.csv": [
        "evidence_dimension",
        "target",
        "horizon_years",
        "pathway_mae",
        "interpretation",
    ],
    "pathway_law_horizon_sweep_v13_4_2026-05-14_city_window.csv": [
        "cutoff_q",
        "horizon_years",
        "train_years",
        "holdout_years",
    ],
    "pathway_law_horizon_sweep_v13_4_2026-05-14_city_window_long.csv": [
        "cutoff_q",
        "horizon_years",
        "train_years",
        "holdout_years",
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
