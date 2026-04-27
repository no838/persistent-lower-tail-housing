# Persistent lower-tail housing reproducibility package

This repository contains the public reproduction code for the manuscript:

> A pathway law for persistent lower-tail housing

The code is designed to reproduce manuscript-level validation results from
analysis-ready research tables. It does not depend on local project paths,
temporary caches, Word exports or private runtime state.

## Scientific target

The manuscript treats persistent lower-tail housing as a dynamic process rather
than a static low-price map. The central pathway expression is:

```text
P ~= X * (1 - lambda) * delta
```

where:

- `P` is the persistent lower-tail share.
- `X` is lower-tail exposure.
- `lambda` is immediate escape after first exposure.
- `1 - lambda` is immediate non-escape.
- `delta` is deepening conditional on repeat exposure.

The scripts reproduce four manuscript-facing validation layers:

- China pathway calibration and exposure-only comparison.
- China transaction-detail validation.
- UK holdout replication.
- France DVF department-frame extension.
- Component attribution summaries for settlement, functional and static sidecars.

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
variables, China transaction-detail validation, UK holdout summaries, France
department-frame extension summaries and component-attribution summaries.

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
france_dvf_department_pathway_smoke_model_summary_2021_2025.csv
france_dvf_department_pathway_smoke_city_table_2021_2025.csv
component_attribution_board_2026-04-23.csv
```

Additional public-release metadata are provided in:

```text
data/release_manifest.csv
data/column_dictionary.csv
data/external_sources.md
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
- UK 12-city holdout win share near `0.8455` for the minimal pathway expression.
- France DVF department-frame extension with Pearson near `0.8327`, Spearman
  near `0.8652`, MAE near `0.0390`, and win share versus exposure-only equal
  to `1.0000`.

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
