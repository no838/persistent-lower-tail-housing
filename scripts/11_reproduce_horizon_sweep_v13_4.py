"""Reproduce horizon-sweep boundary summaries.

This script summarizes the v13.4 horizon-sweep tables that separate the
pathway expression from a short-horizon Markov forecast benchmark. The claim is
bounded: the pathway is not the best short-horizon state forecast, but remains
informative for longer-horizon hardening and exposure-normalized collapse.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from utils import data_file, f, fmt, print_rows, read_csv, write_csv


PERFORMANCE = "pathway_law_horizon_sweep_v13_4_2026-05-14_performance.csv"
COLLAPSE = "pathway_law_horizon_sweep_v13_4_2026-05-14_collapse.csv"
EVIDENCE = "pathway_law_evidence_matrix_v13_4_2026-05-14.csv"


def by_predictor(rows: list[dict[str, str]], horizon: str, target_mode: str) -> dict[str, dict[str, str]]:
    return {
        row.get("predictor", ""): row
        for row in rows
        if row.get("horizon_years") == horizon and row.get("target_mode") == target_mode
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path("data/analysis_ready"))
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/tables"))
    args = parser.parse_args()

    performance = read_csv(data_file(args.data_dir, PERFORMANCE))
    collapse = read_csv(data_file(args.data_dir, COLLAPSE))
    evidence = read_csv(data_file(args.data_dir, EVIDENCE))

    target_mode = "majority_holdout_years"
    majority_rows: list[dict[str, str]] = []
    for horizon in ["1", "2", "3", "4", "5"]:
        row_map = by_predictor(performance, horizon, target_mode)
        pathway = row_map.get("pathway_active", {})
        markov = row_map.get("markov_stationary", {})
        exposure = row_map.get("exposure_only", {})
        p_mae = f(pathway.get("mae"))
        m_mae = f(markov.get("mae"))
        e_mae = f(exposure.get("mae"))
        majority_rows.append(
            {
                "horizon_years": horizon,
                "pathway_mae": fmt(p_mae),
                "markov_stationary_mae": fmt(m_mae),
                "exposure_only_mae": fmt(e_mae),
                "pathway_minus_markov_mae": fmt(p_mae - m_mae if p_mae is not None and m_mae is not None else None),
                "pathway_beats_markov": str(bool(p_mae is not None and m_mae is not None and p_mae < m_mae)),
                "pathway_beats_exposure_only": str(bool(p_mae is not None and e_mae is not None and p_mae < e_mae)),
            }
        )

    collapse_rows = [
        {
            "horizon_years": row.get("horizon_years", ""),
            "target_mode": row.get("target_mode", ""),
            "n": row.get("n", ""),
            "kernel_vs_target_after_exposure_pearson": row.get(
                "kernel_vs_target_after_exposure_pearson", ""
            ),
            "kernel_vs_target_after_exposure_spearman": row.get(
                "kernel_vs_target_after_exposure_spearman", ""
            ),
            "kernel_vs_target_after_exposure_mae": row.get("kernel_vs_target_after_exposure_mae", ""),
        }
        for row in collapse
        if row.get("target_mode") == "majority_holdout_years"
    ]

    write_csv(args.out_dir / "horizon_sweep_majority_mae_summary_v13_4.csv", majority_rows)
    write_csv(args.out_dir / "horizon_sweep_hardening_kernel_collapse_v13_4.csv", collapse_rows)
    write_csv(args.out_dir / "horizon_sweep_evidence_matrix_v13_4.csv", evidence)
    print_rows(majority_rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
