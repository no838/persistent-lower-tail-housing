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
generated from official public transaction sources. The large official raw public
datasets are not redistributed here; source links are listed in:

```text
data/external_sources.md
```

## Data inventory

- `release_manifest.csv` lists the released analysis-ready files, row counts and
  column counts.
- `column_dictionary.csv` lists the columns present in each released CSV file.
- `external_sources.md` records the official public source links for UK HM Land
  Registry, France DVF, SinoBF-1, China building height and ChinaUV++.
