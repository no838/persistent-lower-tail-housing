"""Shared helpers for the public reproducibility scripts."""

from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path
from typing import Iterable


MISSING = {"", "NA", "NaN", "nan", "None", "none", "null", "NULL"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Iterable[dict[str, object]]) -> None:
    rows = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def f(value: object) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if text in MISSING:
        return None
    try:
        out = float(text)
    except ValueError:
        return None
    if math.isnan(out):
        return None
    return out


def truthy(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "t", "yes", "y"}


def get(row: dict[str, str], *names: str, default: str = "") -> str:
    for name in names:
        if name in row and row[name] not in MISSING:
            return row[name]
    return default


def require_columns(path: Path, rows: list[dict[str, str]], columns: list[str]) -> list[str]:
    if not rows:
        return columns
    available = set(rows[0])
    return [column for column in columns if column not in available]


def data_file(data_dir: Path, filename: str) -> Path:
    return data_dir / filename


def pairs(xs: Iterable[object], ys: Iterable[object]) -> tuple[list[float], list[float]]:
    out_x: list[float] = []
    out_y: list[float] = []
    for x_raw, y_raw in zip(xs, ys):
        x = f(x_raw)
        y = f(y_raw)
        if x is None or y is None:
            continue
        out_x.append(x)
        out_y.append(y)
    return out_x, out_y


def pearson(xs: Iterable[object], ys: Iterable[object]) -> float | None:
    x, y = pairs(xs, ys)
    n = len(x)
    if n < 2:
        return None
    mx = sum(x) / n
    my = sum(y) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(x, y))
    vx = sum((a - mx) ** 2 for a in x)
    vy = sum((b - my) ** 2 for b in y)
    if vx <= 0 or vy <= 0:
        return None
    return cov / math.sqrt(vx * vy)


def average_ranks(values: list[float]) -> list[float]:
    indexed = sorted(enumerate(values), key=lambda item: item[1])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(indexed):
        j = i
        while j + 1 < len(indexed) and indexed[j + 1][1] == indexed[i][1]:
            j += 1
        rank = (i + 1 + j + 1) / 2.0
        for k in range(i, j + 1):
            ranks[indexed[k][0]] = rank
        i = j + 1
    return ranks


def spearman(xs: Iterable[object], ys: Iterable[object]) -> float | None:
    x, y = pairs(xs, ys)
    if len(x) < 2:
        return None
    return pearson(average_ranks(x), average_ranks(y))


def mae(xs: Iterable[object], ys: Iterable[object]) -> float | None:
    x, y = pairs(xs, ys)
    if not x:
        return None
    return sum(abs(a - b) for a, b in zip(x, y)) / len(x)


def fmt(value: float | None, digits: int = 6) -> str:
    if value is None:
        return "NA"
    return f"{value:.{digits}f}"


def group_by(rows: Iterable[dict[str, str]], key: str) -> dict[str, list[dict[str, str]]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[row.get(key, "")].append(row)
    return dict(groups)


def print_rows(rows: list[dict[str, object]]) -> None:
    for row in rows:
        print(", ".join(f"{key}={value}" for key, value in row.items()))

