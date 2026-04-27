"""Export component-attribution rows used in the manuscript narrative."""

from __future__ import annotations

import argparse
from pathlib import Path

from utils import data_file, print_rows, read_csv, write_csv


BOARD = "component_attribution_board_2026-04-23.csv"
KEY_SIGNALS = {
    "urban-village proximity",
    "roof density",
    "population exposure",
    "dense-hardening selector",
    "newer build",
    "lower fee",
    "lower plot",
    "SinoBF-1 orientation",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path("data/analysis_ready"))
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/tables"))
    args = parser.parse_args()

    rows = read_csv(data_file(args.data_dir, BOARD))
    key_rows = [row for row in rows if row.get("signal") in KEY_SIGNALS]
    compact_rows = [
        {
            "layer": row.get("layer", ""),
            "signal": row.get("signal", ""),
            "exposure_score": row.get("exposure_score", ""),
            "hardening_score": row.get("hardening_score", ""),
            "phase_or_residual_score": row.get("phase_or_residual_score", ""),
            "primary_component": row.get("primary_component", ""),
            "formula_role": row.get("formula_role", ""),
        }
        for row in key_rows
    ]

    write_csv(args.out_dir / "component_attribution_key_rows.csv", compact_rows)
    print_rows(compact_rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

