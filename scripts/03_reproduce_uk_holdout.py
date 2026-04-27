"""Reproduce UK holdout model-ordering summaries."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from utils import data_file, f, group_by, print_rows, read_csv, write_csv


SUMMARY_12 = "uk_all_available12_holdout_transfer_summary_2026-04-23.csv"
SPLITS_12 = "uk_all_available12_holdout_split_table_2026-04-23.csv"
SUMMARY_TOP10 = "uk_top10_holdout_transfer_summary_2026-04-23.csv"


def split_winners(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    winners = []
    for split_id, split_rows in group_by(rows, "split_id").items():
        scored = [(row.get("model", ""), f(row.get("holdout_mae"))) for row in split_rows]
        scored = [(model, value) for model, value in scored if value is not None]
        if not scored:
            continue
        model, value = min(scored, key=lambda item: item[1])
        winners.append({"split_id": split_id, "winner": model, "winning_holdout_mae": value})
    return winners


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path("data/analysis_ready"))
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/tables"))
    args = parser.parse_args()

    summary_rows = read_csv(data_file(args.data_dir, SUMMARY_12))
    split_rows = read_csv(data_file(args.data_dir, SPLITS_12))
    top10_path = data_file(args.data_dir, SUMMARY_TOP10)
    top10_rows = read_csv(top10_path) if top10_path.exists() else []

    winners = split_winners(split_rows)
    counts = Counter(row["winner"] for row in winners)
    n = len(winners)
    winner_summary = [
        {
            "model": model,
            "split_win_count": counts.get(model, 0),
            "split_win_share": counts.get(model, 0) / n if n else "",
        }
        for model in sorted({row.get("model", "") for row in split_rows})
    ]

    all_summary = []
    for frame, rows in [("all_available_12_city", summary_rows), ("top10_power_screened", top10_rows)]:
        for row in rows:
            all_summary.append({"frame": frame, **row})

    write_csv(args.out_dir / "uk_holdout_model_summary.csv", all_summary)
    write_csv(args.out_dir / "uk_holdout_split_winners.csv", winners)
    write_csv(args.out_dir / "uk_holdout_winner_summary_from_splits.csv", winner_summary)
    print_rows(winner_summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

