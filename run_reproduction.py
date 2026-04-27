"""Run the public manuscript-level reproduction scripts."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


TABLE_SCRIPTS = [
    "00_check_inputs.py",
    "01_reproduce_pathway_results.py",
    "02_reproduce_china_transaction_validation.py",
    "03_reproduce_uk_holdout.py",
    "04_reproduce_france_extension.py",
    "05_reproduce_component_attribution.py",
]


def run(script: Path, data_dir: Path, out_dir: Path) -> None:
    cmd = [sys.executable, str(script), "--data-dir", str(data_dir)]
    if script.name != "00_check_inputs.py":
        cmd.extend(["--out-dir", str(out_dir)])
    print("\nRunning:", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path("data/analysis_ready"))
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/tables"))
    parser.add_argument(
        "--with-figures",
        action="store_true",
        help="also build lightweight diagnostic PNGs with matplotlib",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    scripts_dir = root / "scripts"
    data_dir = args.data_dir if args.data_dir.is_absolute() else root / args.data_dir
    out_dir = args.out_dir if args.out_dir.is_absolute() else root / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    for name in TABLE_SCRIPTS:
        run(scripts_dir / name, data_dir, out_dir)

    if args.with_figures:
        fig_dir = root / "outputs" / "figures"
        cmd = [
            sys.executable,
            str(scripts_dir / "06_build_diagnostic_figures.py"),
            "--data-dir",
            str(data_dir),
            "--fig-dir",
            str(fig_dir),
        ]
        print("\nRunning:", " ".join(cmd))
        subprocess.run(cmd, check=True)

    print("\nReproduction scripts completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
