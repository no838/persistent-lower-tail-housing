# Persistent lower-tail housing reproducibility package

This repository contains the public reproduction code for the manuscript:

> How lower-tail exposure becomes persistent housing disadvantage

The code is designed to reproduce manuscript-level validation results from
analysis-ready research tables. It does not depend on local project paths,
temporary caches, Word exports or private runtime state.

## Scientific target

The manuscript treats persistent lower-tail housing as a dynamic process rather
than a static low-price map. The central pathway expression is:

```text
P ≈ X × (1 - λ) × δ
```

where:

- `P` is the persistent lower-tail share.
- `X` is lower-tail exposure.
- `λ` is immediate escape after first exposure.
- `1 - λ` is immediate non-escape.
- `δ` is deepening conditional on repeat exposure.

The v13.5 manuscript treats this expression as process accounting rather than as
a universally dominant forecast law. Temporal forecast checks with future years
withheld show that the expression is not merely an in-window identity, but a
Markov-pair retention kernel is the stricter short-horizon benchmark for
two-year repeat lower-tail forecasts. A later horizon sweep keeps this boundary
explicit: Markov is sharper at two- and three-year majority-persistence horizons,
whereas the pathway expression overtakes Markov at four- and five-year horizons
and preserves exposure-normalized hardening-kernel collapse.

The scripts reproduce manuscript-facing validation layers:

- China pathway calibration and exposure-only comparison.
- China transaction-detail validation.
- UK holdout replication and ONSPD-linked England-Wales frame-relative replication.
- France DVF department-frame extension.
- Component attribution summaries for settlement, functional and static sidecars.
- China broad 20-city internal robustness frame, kept separate from the
  canonical 12-city calibration frame.
- v13 temporal anti-identity forecast checks.
- v13.1 threshold-policy, component-uncertainty and leave-one-city summaries.
- v13.4 horizon-sweep boundary checks.

## Repository layout

```text
persistent_lower_tail_housing_reproducibility/
  README.md
  requirements.txt
  run_reproduction.py
  data/
    README.md
    analysis_ready/
  scripts/
    00_check_inputs.py
    01_reproduce_pathway_results.py
    02_reproduce_china_transaction_validation.py
    03_reproduce_uk_holdout.py
    04_reproduce_france_extension.py
    05_reproduce_component_attribution.py
    06_build_diagnostic_figures.py
    07_reproduce_uk_cityframe.py
    08_reproduce_temporal_forecast.py
    09_reproduce_uncertainty_threshold_policy.py
    10_reproduce_china_broad20_robustness.py
    11_reproduce_horizon_sweep_v13_4.py
    utils.py
  outputs/
    tables/
    figures/
```

## Data included in this release

The folder already includes manuscript-level analysis-ready tables in:

```text
data/analysis_ready/
```

These are compact research tables used to reproduce the reported pathway
variables, China transaction-detail validation, UK holdout summaries,
ONSPD-linked England-Wales frame summaries, France department-frame extension
summaries and component-attribution summaries.

The package includes:

```text
universal_pathway_law_city_table_2026-04-20.csv
community_transition_process_2018_2022.csv
city_transition_process_decomposition_2018_2022.csv
china_transaction_detail_validation_expansion_city_summary_2026-04-23.csv
china_transaction_detail_validation_expansion_pair_scores_2026-04-23.csv
uk_all_available12_holdout_transfer_summary_2026-04-23.csv
uk_all_available12_holdout_split_table_2026-04-23.csv
uk_top10_holdout_transfer_summary_2026-04-23.csv
uk_cityframe_performance_summary_2018_2022.csv
uk_cityframe_pathway_metrics_2018_2022.csv
uk_cityframe_panel_coverage_2018_2022.csv
uk_old_vs_cityframe_performance_comparison_2018_2022.csv
broad20_city_pathway_law_table_2018_2022.csv
china_internal_holdout_replication_broad20_model_summary_2026-04-21.csv
china_internal_holdout_replication_broad20_split_table_2026-04-21.csv
china_internal_holdout_replication_broad20_transfer_summary_2026-04-21.csv
france_dvf_department_pathway_smoke_model_summary_2021_2025.csv
france_dvf_department_pathway_smoke_city_table_2021_2025.csv
component_attribution_board_2026-04-23.csv
china_early_window_forecast_performance_v13_2026-05-14.csv
china_early_window_forecast_permutation_null_v13_2026-05-14.csv
china_rolling_origin_forecast_performance_v13_2026-05-14.csv
pathway_components_uncertainty_v13_1_2026-05-14.csv
pathway_forecast_city_jackknife_v13_1_2026-05-14.csv
threshold_policy_and_sensitivity_v13_1_2026-05-14.csv
pathway_law_horizon_sweep_v13_4_2026-05-14_performance.csv
pathway_law_horizon_sweep_v13_4_2026-05-14_collapse.csv
pathway_law_evidence_matrix_v13_4_2026-05-14.csv
pathway_law_horizon_sweep_v13_4_2026-05-14_city_window.csv
pathway_law_horizon_sweep_v13_4_2026-05-14_city_window_long.csv
```

Additional public-release metadata are provided in:

```text
data/release_manifest.csv
data/column_dictionary.csv
data/external_sources.md
data/uk_onspd_cityframe_provenance.md
```

The China transaction-detail tables include only research fields needed for
validation. Personal identifiers and non-research fields are not included.

## Quick start

Create a clean environment and install optional plotting support:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Check the included input files:

```bash
python scripts/00_check_inputs.py --data-dir data/analysis_ready
```

Run all table reproductions:

```bash
python run_reproduction.py --data-dir data/analysis_ready --out-dir outputs/tables
```

Run the optional diagnostic figure builder:

```bash
python scripts/06_build_diagnostic_figures.py \
  --data-dir data/analysis_ready \
  --fig-dir outputs/figures
```

## Expected headline outputs

The released tables should reproduce the manuscript-level results, including:

- Pathway calibration near `r = 0.963` and `MAE = 0.0037`.
- China transaction-detail validation with `6/6` positive city rank gaps,
  `43/43` available matched pairs concordant, and `42/42` strict-only pairs
  concordant.
- UK 12-city holdout win share near `0.8455` for the older minimal pathway
  diagnostic.
- China broad 20-city internal robustness outputs are reproduced as a separate
  robustness frame. They are not the main calibration frame and are used to
  check whether the pathway ordering persists beyond the canonical 12-city
  balanced panel.
- ONSPD-linked England-Wales frame-relative results in which the pathway expression
  beats exposure-only across TTWA, LAD and BUA frames; available-cohort MAE is
  `0.0260` versus `0.1028` for TTWA, `0.0347` versus `0.1493` for LAD, and
  `0.0461` versus `0.1790` for BUA.
- France DVF department-frame extension with Pearson near `0.8327`, Spearman
  near `0.8652`, MAE near `0.0390`, and win share versus exposure-only equal
  to `1.0000`.
- v13 temporal anti-identity checks: the `2018-2020` to `2021-2022` split gives
  pathway MAE `0.0213` versus exposure-only `0.1114` and sequence-permutation
  median MAE `0.0453`; rolling origins over `2010-2022` give pathway MAE
  `0.0146` versus exposure-only `0.0935`. Markov-pair retention remains lower
  error for the short two-year repeat target.
- v13.1 uncertainty and threshold-policy checks: the single-split pathway MAE
  has 95% bootstrap CI `0.0141-0.0303`; the rolling-origin pathway MAE has
  city-cluster bootstrap CI `0.0114-0.0202`; leave-one-city checks preserve the
  pathway-over-exposure ordering in every main run; China bottom decile is the
  discovery definition while England-Wales and France are bottom-`20%`
  frame-relative extensions.
- v13.4 horizon-sweep checks: Markov retention remains better at two- and
  three-year majority-persistence horizons, while the pathway expression beats
  Markov at four- and five-year horizons and the hardening-kernel collapse
  remains strong after exposure normalization.

Small differences in printed rounding are expected.

## What this package is and is not

This package is a reproducibility scaffold for manuscript-level results. It is
not the full local project workspace, not the raw-data downloader system and not
the Word manuscript builder. It is intentionally smaller so that reviewers and
readers can inspect the analysis-ready validation logic without local paths or
runtime cache state.

## Licence

Repository software code is released under the MIT License. Analysis-ready
research tables released in `data/analysis_ready/`, `data/release_manifest.csv`
and `data/column_dictionary.csv` are released under CC BY 4.0 unless otherwise
stated. External public datasets listed in `data/external_sources.md` remain
under their original licences and terms of use.

## Citation

If you use this code, cite the associated manuscript and the archived release of
this repository.
