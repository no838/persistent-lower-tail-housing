# Data release

The package includes analysis-ready CSV files released with the manuscript in:

```text
data/analysis_ready/
```

These are research tables, not raw private exports. The China transaction-detail
release contains cleaned validation records, matching tiers, city summaries and
matched-pair tables needed to reproduce the reported rank gaps and concordance
results. Personal identifiers and non-research fields are excluded.

The public UK and France scripts operate on compact analysis-ready tables
generated from official public transaction sources. The ONSPD-linked
England-Wales frame release includes frame-level performance, pathway metrics,
panel coverage and old-vs-new comparison tables; it does not redistribute full
postcode lookup tables or raw transaction records. The large official raw public
datasets are not redistributed here; source links are listed in:

```text
data/external_sources.md
```

## Data inventory

- `release_manifest.csv` lists the released analysis-ready files, row counts and
  column counts.
- `column_dictionary.csv` lists the columns present in each released CSV file.
- `external_sources.md` records the official public source links for UK HM Land
  Registry, ONSPD, France DVF, SinoBF-1, China building height and ChinaUV++.
- `broad20_city_pathway_law_table_2018_2022.csv` and
  `china_internal_holdout_replication_broad20_*` files record the broader
  20-city internal robustness frame. The 12-city table remains the canonical
  pathway calibration frame; the broad 20-city files are included so readers can
  reproduce the manuscript's internal robustness and timing-sensitivity claims.
- `uk_onspd_cityframe_provenance.md` records the included England-Wales ONSPD-derived
  tables, excluded larger lookup/panel files and claim boundaries.
- `china_early_window_forecast_*v13*` and
  `china_rolling_origin_forecast_*v13*` record the temporal anti-identity
  forecast checks used to distinguish process accounting from an in-window
  probability decomposition.
- `pathway_components_uncertainty_v13_1_2026-05-14.csv`,
  `pathway_forecast_city_jackknife_v13_1_2026-05-14.csv` and
  `threshold_policy_and_sensitivity_v13_1_2026-05-14.csv` record the v13.1
  component-uncertainty, leave-one-city and threshold-policy checks used in the
  manuscript Methods and robustness boundary.
