"""Reproduce France DVF department-frame extension summaries."""

from __future__ import annotations

import argparse
from pathlib import Path

from utils import data_file, fmt, mae, pearson, print_rows, read_csv, spearman, truthy, write_csv


MODEL_SUMMARY = "france_dvf_department_pathway_smoke_model_summary_2021_2025.csv"
DEPARTMENT_TABLE = "france_dvf_department_pathway_smoke_city_table_2021_2025.csv"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path("data/analysis_ready"))
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/tables"))
    args = parser.parse_args()

    model_rows = read_csv(data_file(args.data_dir, MODEL_SUMMARY))
    department_rows = read_csv(data_file(args.data_dir, DEPARTMENT_TABLE))

    observed = [row["persistent_share_3plus"] for row in department_rows]
    minimal = [row["minimal_law_prediction"] for row in department_rows]
    exposure = [row["exposure_only_prediction"] for row in department_rows]
    wins = sum(1 for row in department_rows if truthy(row.get("minimal_beats_exposure_only")))
    n = len(department_rows)

    recomputed = [
        {"metric": "department_frames", "value": n},
        {"metric": "minimal_law_pearson_recomputed", "value": fmt(pearson(minimal, observed))},
        {"metric": "minimal_law_spearman_recomputed", "value": fmt(spearman(minimal, observed))},
        {"metric": "minimal_law_mae_recomputed", "value": fmt(mae(minimal, observed))},
        {"metric": "exposure_only_mae_recomputed", "value": fmt(mae(exposure, observed))},
        {"metric": "minimal_law_win_share_vs_exposure_only_recomputed", "value": fmt(wins / n if n else None)},
    ]

    write_csv(args.out_dir / "france_extension_model_summary.csv", model_rows)
    write_csv(args.out_dir / "france_extension_recomputed_summary.csv", recomputed)
    print_rows(recomputed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

