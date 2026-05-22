"""Reproduce UK ONSPD-linked city-frame performance summaries."""

from __future__ import annotations

import argparse
from pathlib import Path

from utils import data_file, f, group_by, print_rows, read_csv, write_csv


PERFORMANCE = "uk_cityframe_performance_summary_2018_2022.csv"
METRICS = "uk_cityframe_pathway_metrics_2018_2022.csv"
COVERAGE = "uk_cityframe_panel_coverage_2018_2022.csv"
OLD_VS_NEW = "uk_old_vs_cityframe_performance_comparison_2018_2022.csv"


def frame_summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for row in rows:
        mae_pathway = f(row.get("mae_pathway"))
        mae_exposure = f(row.get("mae_exposure_only"))
        out.append(
            {
                "frame_type": row.get("frame_type", ""),
                "cohort_type": row.get("cohort_type", ""),
                "n_frames": row.get("n_frames", ""),
                "mae_pathway": mae_pathway,
                "mae_exposure_only": mae_exposure,
                "pathway_beats_exposure_only": (
                    mae_pathway < mae_exposure
                    if mae_pathway is not None and mae_exposure is not None
                    else ""
                ),
                "relative_mae_reduction": f(row.get("relative_mae_reduction")),
                "pearson_pathway": f(row.get("pearson_pathway")),
                "spearman_pathway": f(row.get("spearman_pathway")),
            }
        )
    return out


def best_frames(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for cohort, cohort_rows in group_by(rows, "cohort_type").items():
        scored = [
            (f(row.get("mae_pathway")), row)
            for row in cohort_rows
            if f(row.get("mae_pathway")) is not None
        ]
        if not scored:
            continue
        _, row = min(scored, key=lambda item: item[0])
        out.append(
            {
                "cohort_type": cohort,
                "best_frame_by_pathway_mae": row.get("frame_type", ""),
                "n_frames": row.get("n_frames", ""),
                "mae_pathway": f(row.get("mae_pathway")),
                "mae_exposure_only": f(row.get("mae_exposure_only")),
                "relative_mae_reduction": f(row.get("relative_mae_reduction")),
            }
        )
    return out


def metrics_rollup(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for key, key_rows in group_by(rows, "frame_type").items():
        by_cohort = group_by(key_rows, "cohort_type")
        for cohort, cohort_rows in by_cohort.items():
            abs_errors = [f(row.get("absolute_error_pathway")) for row in cohort_rows]
            abs_errors = [value for value in abs_errors if value is not None]
            exposure_errors = [f(row.get("absolute_error_exposure_only")) for row in cohort_rows]
            exposure_errors = [value for value in exposure_errors if value is not None]
            out.append(
                {
                    "frame_type": key,
                    "cohort_type": cohort,
                    "n_frame_rows": len(cohort_rows),
                    "mean_absolute_error_pathway_from_metrics": (
                        sum(abs_errors) / len(abs_errors) if abs_errors else ""
                    ),
                    "mean_absolute_error_exposure_only_from_metrics": (
                        sum(exposure_errors) / len(exposure_errors) if exposure_errors else ""
                    ),
                }
            )
    return out


def comparison_rows(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for row in rows:
        out.append(
            {
                "validation_version": row.get("validation_version", ""),
                "frame_type": row.get("frame_type", ""),
                "cohort_type": row.get("cohort_type", ""),
                "n_frames": row.get("n_frames", ""),
                "mae_pathway": f(row.get("mae_pathway")),
                "mae_exposure_only": f(row.get("mae_exposure_only")),
                "relative_mae_reduction": f(row.get("relative_mae_reduction")),
            }
        )
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path("data/analysis_ready"))
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/tables"))
    args = parser.parse_args()

    performance = read_csv(data_file(args.data_dir, PERFORMANCE))
    metrics = read_csv(data_file(args.data_dir, METRICS))
    coverage = read_csv(data_file(args.data_dir, COVERAGE))
    old_vs_new = read_csv(data_file(args.data_dir, OLD_VS_NEW))

    summary = frame_summary(performance)
    best = best_frames(performance)
    rollup = metrics_rollup(metrics)
    comparison = comparison_rows(old_vs_new)

    write_csv(args.out_dir / "uk_cityframe_model_summary.csv", summary)
    write_csv(args.out_dir / "uk_cityframe_best_frames.csv", best)
    write_csv(args.out_dir / "uk_cityframe_metric_rollup.csv", rollup)
    write_csv(args.out_dir / "uk_old_vs_cityframe_performance_comparison.csv", comparison)
    write_csv(args.out_dir / "uk_cityframe_panel_coverage.csv", coverage)

    print_rows(best)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
