"""Reproduce China transaction-detail validation summaries."""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

from utils import data_file, f, fmt, print_rows, read_csv, truthy, write_csv


CITY_SUMMARY = "china_transaction_detail_validation_expansion_city_summary_2026-04-23.csv"
PAIR_SCORES = "china_transaction_detail_validation_expansion_pair_scores_2026-04-23.csv"
STRICT_TIER = "city_area_community"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path("data/analysis_ready"))
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/tables"))
    args = parser.parse_args()

    city_rows = read_csv(data_file(args.data_dir, CITY_SUMMARY))
    pair_rows = read_csv(data_file(args.data_dir, PAIR_SCORES))

    city_gaps = [f(row.get("never_minus_persistent_rank_gap")) for row in city_rows]
    city_gaps = [gap for gap in city_gaps if gap is not None]
    positive_city_gaps = sum(1 for gap in city_gaps if gap > 0)

    available_pairs = [row for row in pair_rows if truthy(row.get("both_external_available"))]
    concordant_pairs = [
        row for row in available_pairs if truthy(row.get("persistent_lower_than_control_external"))
    ]
    strict_pairs = [
        row
        for row in available_pairs
        if row.get("persistent_match_tier") == STRICT_TIER and row.get("control_match_tier") == STRICT_TIER
    ]
    strict_concordant = [
        row for row in strict_pairs if truthy(row.get("persistent_lower_than_control_external"))
    ]

    metrics = [
        {"metric": "cities_with_transaction_rank_gap", "value": len(city_gaps)},
        {"metric": "positive_city_rank_gaps", "value": positive_city_gaps},
        {"metric": "matched_pair_rows", "value": len(pair_rows)},
        {"metric": "available_external_pairs", "value": len(available_pairs)},
        {"metric": "concordant_external_pairs", "value": len(concordant_pairs)},
        {"metric": "strict_available_pairs", "value": len(strict_pairs)},
        {"metric": "strict_concordant_pairs", "value": len(strict_concordant)},
    ]

    by_city: dict[str, dict[str, int]] = defaultdict(
        lambda: {
            "available_pairs": 0,
            "concordant_pairs": 0,
            "strict_available_pairs": 0,
            "strict_concordant_pairs": 0,
        }
    )
    for row in available_pairs:
        city = row.get("city", "")
        by_city[city]["available_pairs"] += 1
        if truthy(row.get("persistent_lower_than_control_external")):
            by_city[city]["concordant_pairs"] += 1
        if row.get("persistent_match_tier") == STRICT_TIER and row.get("control_match_tier") == STRICT_TIER:
            by_city[city]["strict_available_pairs"] += 1
            if truthy(row.get("persistent_lower_than_control_external")):
                by_city[city]["strict_concordant_pairs"] += 1

    city_output = []
    city_gap_lookup = {
        row.get("city", ""): row.get("never_minus_persistent_rank_gap", "") for row in city_rows
    }
    for city, counts in sorted(by_city.items()):
        city_output.append(
            {
                "city": city,
                "never_minus_persistent_rank_gap": city_gap_lookup.get(city, ""),
                **counts,
            }
        )

    write_csv(args.out_dir / "china_transaction_validation_summary.csv", metrics)
    write_csv(args.out_dir / "china_transaction_validation_by_city.csv", city_output)
    print_rows(metrics)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

