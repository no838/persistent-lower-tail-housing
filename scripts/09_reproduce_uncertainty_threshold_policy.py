"""Reproduce v13.1 uncertainty, jackknife and threshold-policy summaries."""

from __future__ import annotations

import argparse
from pathlib import Path

from utils import data_file, f, fmt, read_csv, write_csv


COMPONENTS = "pathway_components_uncertainty_v13_1_2026-05-14.csv"
JACKKNIFE = "pathway_forecast_city_jackknife_v13_1_2026-05-14.csv"
THRESHOLD = "threshold_policy_and_sensitivity_v13_1_2026-05-14.csv"


def find_row(rows: list[dict[str, str]], **criteria: object) -> dict[str, str]:
    for row in rows:
        ok = True
        for key, expected in criteria.items():
            value = row.get(key)
            if isinstance(expected, float):
                got = f(value)
                ok = got is not None and abs(got - expected) < 1e-9
            else:
                ok = value == str(expected)
            if not ok:
                break
        if ok:
            return row
    raise ValueError(f"missing row: {criteria}")


def boolish(value: object) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def jackknife_summary(rows: list[dict[str, str]], test: str, q: float) -> dict[str, str]:
    subset = [
        row
        for row in rows
        if row.get("test") == test
        and row.get("left_out_city") != "__FULL_SAMPLE__"
        and f(row.get("cutoff_q")) is not None
        and abs(f(row.get("cutoff_q")) - q) < 1e-9
    ]
    if not subset:
        raise ValueError(f"missing jackknife rows for {test} {q}")
    pathway_maes = [f(row.get("pathway_mae")) for row in subset]
    pathway_maes = [value for value in pathway_maes if value is not None]
    return {
        "test": test,
        "cutoff_q": fmt(q),
        "n_leave_one_city_runs": str(len(subset)),
        "pathway_beats_exposure_share": fmt(
            sum(boolish(row.get("pathway_beats_exposure_only")) for row in subset) / len(subset)
        ),
        "markov_beats_pathway_share": fmt(
            sum(boolish(row.get("markov_beats_pathway")) for row in subset) / len(subset)
        ),
        "pathway_mae_min": fmt(min(pathway_maes)),
        "pathway_mae_max": fmt(max(pathway_maes)),
    }


def component_summary(rows: list[dict[str, str]], test: str, q: float, component: str) -> dict[str, str]:
    row = find_row(rows, test=test, cutoff_q=q, component=component)
    return {
        "test": test,
        "cutoff_q": fmt(q),
        "component": component,
        "mean_unweighted": row.get("mean_unweighted", "NA"),
        "bootstrap_mean_ci_low": row.get("bootstrap_mean_ci_low", "NA"),
        "bootstrap_mean_ci_high": row.get("bootstrap_mean_ci_high", "NA"),
        "n_cities": row.get("n_cities", "NA"),
    }


def threshold_summary(rows: list[dict[str, str]], test: str, q: float, predictor: str) -> dict[str, str]:
    row = find_row(rows, test=test, cutoff_q=q, predictor=predictor)
    return {
        "test": test,
        "cutoff_q": fmt(q),
        "predictor": predictor,
        "mae": row.get("mae", "NA"),
        "mae_ci_low": row.get("mae_ci_low", "NA"),
        "mae_ci_high": row.get("mae_ci_high", "NA"),
        "relative_mae_reduction_vs_exposure_only": row.get("relative_mae_reduction_vs_exposure_only", "NA"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path("data/analysis_ready"))
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/tables"))
    args = parser.parse_args()

    components = read_csv(data_file(args.data_dir, COMPONENTS))
    jackknife = read_csv(data_file(args.data_dir, JACKKNIFE))
    threshold = read_csv(data_file(args.data_dir, THRESHOLD))

    rows: list[dict[str, str]] = []
    for test in ["single_split_2018_2020_to_2021_2022", "rolling_origin_2010_2022"]:
        rows.append({"section": "jackknife", **jackknife_summary(jackknife, test, 0.10)})
        for component in ["X", "lambda", "non_escape", "delta_active", "markov_p11"]:
            rows.append({"section": "component_uncertainty", **component_summary(components, test, 0.10, component)})
        for predictor in ["pathway_active", "markov_pair", "exposure_only", "independence"]:
            rows.append({"section": "threshold_policy", **threshold_summary(threshold, test, 0.10, predictor)})

    write_csv(args.out_dir / "uncertainty_threshold_policy_summary_v13_1.csv", rows)
    for row in rows:
        print(", ".join(f"{key}={value}" for key, value in row.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
