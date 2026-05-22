# UK ONSPD-linked city-frame provenance

Date added to release package: 2026-05-14

## Purpose

This note documents the compact UK ONSPD-linked analysis-ready tables included
in this public reproducibility package. These tables support the manuscript
claim that England-Wales HM Land Registry transactions linked through ONSPD
postcode geography reproduce the pathway ordering across administrative,
labour-market and built-up-area frames.

## Public source inputs

- HM Land Registry Price Paid Data, yearly price-paid transaction files.
- ONS Postcode Directory (February 2026) for the UK (Hosted Table), used for
  full postcode to LAD / TTWA / BUA frame mapping.

## Derived release tables

The release tables are compact analysis-ready derivatives generated from the
public source inputs above. The local build workspace is not part of the public
release because reproduction uses the included CSV tables and scripts.

Included files:

- uk_cityframe_performance_summary_2018_2022.csv
- uk_cityframe_pathway_metrics_2018_2022.csv
- uk_cityframe_panel_coverage_2018_2022.csv
- uk_old_vs_cityframe_performance_comparison_2018_2022.csv

## Release exclusions

The following local files are not included in the public release package:

- uk_postcode_to_frame_lookup.csv
- uk_postcode_district_to_modal_frame_lookup.csv
- uk_cityframe_unit_year_price_panel_2018_2022.csv
- uk_cityframe_unit_year_lower_tail_panel_2018_2022.csv

The exclusion is intentional. The manuscript-level claim only requires
frame-level performance, pathway metrics and coverage summaries. Full postcode
lookup tables and unit-year transaction panels are larger derived products and
should remain outside the compact release unless redistribution/licence and
privacy review explicitly approve them.

## Coverage summary

The included performance summary has six rows:

- LAD, TTWA and BUA frames.
- Available and balanced cohorts.
- Pathway and exposure-only error metrics.

The included pathway metrics table has 574 frame-cohort rows. The coverage
table records price-panel frame counts and retained transaction counts. The
old-vs-new comparison table preserves the older postcode-area diagnostic as a
robustness context rather than the headline UK evidence.

## Claim boundary

Use this wording:

ONSPD-linked England-Wales transaction data reproduce the pathway ordering
across administrative, labour-market and built-up-area frames.

Do not call this a nationwide UK replication. HM Land Registry Price Paid Data
cover England and Wales, and ONSPD February 2026 geography is used as a
consistent postcode-to-frame mapping for the 2018-2022 transaction window.

## Reproduction command

python scripts/07_reproduce_uk_cityframe.py --data-dir data/analysis_ready --out-dir outputs/tables

The script writes:

- outputs/tables/uk_cityframe_model_summary.csv
- outputs/tables/uk_cityframe_best_frames.csv
- outputs/tables/uk_cityframe_metric_rollup.csv
- outputs/tables/uk_old_vs_cityframe_performance_comparison.csv
- outputs/tables/uk_cityframe_panel_coverage.csv
