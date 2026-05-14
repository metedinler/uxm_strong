#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Downloads altindaki BAS/BI dosyalari icin envanter CSV uretir.

Not: CSV yazimi icin once mevcut Stage-20 aracindaki write_csv yardimcisini kullanmayi dener.
Bulunamazsa standart csv.DictWriter ile devam eder.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import re
from pathlib import Path
from datetime import datetime


def load_stage20_writer(repo_root: Path):
    script = (
        repo_root
        / "tools"
        / "release_gate_v20"
        / "UXM_V33_FINAL_RELEASE_GATE_V20_PACKAGE"
        / "araclar"
        / "uxm_stage20_final.py"
    )
    if not script.exists():
        return None

    spec = importlib.util.spec_from_file_location("uxm_stage20_final", script)
    if spec is None or spec.loader is None:
        return None

    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "write_csv", None)


def safe_read_text(path: Path) -> str:
    for enc in ("utf-8-sig", "utf-8", "cp1254", "latin-1"):
        try:
            return path.read_text(encoding=enc, errors="replace")
        except Exception:
            continue
    return ""


def summarize_content(text: str) -> dict:
    lines = text.splitlines()
    first_nonempty = ""
    for ln in lines:
        s = ln.strip()
        if s:
            first_nonempty = s[:180]
            break

    include_count = len(re.findall(r"(?im)^\s*#include\b", text))
    declare_count = len(re.findall(r"(?im)^\s*declare\b", text))
    type_count = len(re.findall(r"(?im)^\s*type\b", text))
    function_count = len(re.findall(r"(?im)^\s*function\b", text))
    sub_count = len(re.findall(r"(?im)^\s*sub\b", text))
    const_count = len(re.findall(r"(?im)^\s*const\b", text))

    info = (
        f"include={include_count}; declare={declare_count}; type={type_count}; "
        f"function={function_count}; sub={sub_count}; const={const_count}"
    )

    return {
        "line_count": len(lines),
        "first_nonempty": first_nonempty,
        "include_count": include_count,
        "declare_count": declare_count,
        "type_count": type_count,
        "function_count": function_count,
        "sub_count": sub_count,
        "const_count": const_count,
        "content_info": info,
    }


def fmt_ts(ts: float) -> str:
    try:
        return datetime.fromtimestamp(ts).isoformat(sep=" ", timespec="seconds")
    except Exception:
        return ""


def build_rows(scan_root: Path) -> list[dict]:
    rows: list[dict] = []
    for p in scan_root.rglob("*"):
        if not p.is_file():
            continue
        ext = p.suffix.lower()
        if ext not in (".bas", ".bi"):
            continue

        st = p.stat()
        text = safe_read_text(p)
        meta = summarize_content(text)

        rows.append(
            {
                "full_path": str(p),
                "relative_path": str(p.relative_to(scan_root)),
                "folder": str(p.parent),
                "extension": ext,
                "size_bytes": st.st_size,
                "created_at": fmt_ts(st.st_ctime),
                "modified_at": fmt_ts(st.st_mtime),
                "line_count": meta["line_count"],
                "include_count": meta["include_count"],
                "declare_count": meta["declare_count"],
                "type_count": meta["type_count"],
                "function_count": meta["function_count"],
                "sub_count": meta["sub_count"],
                "const_count": meta["const_count"],
                "first_nonempty": meta["first_nonempty"],
                "content_info": meta["content_info"],
            }
        )

    rows.sort(key=lambda r: (r["folder"], r["relative_path"]))
    return rows


def write_csv_fallback(out_csv: Path, rows: list[dict], fields: list[str]) -> None:
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", encoding="utf-8-sig", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        wr.writeheader()
        wr.writerows(rows)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="BAS/BI envanter CSV uretici")
    ap.add_argument(
        "--scan-root",
        default=r"C:\Users\mete\Downloads",
        help="Taranacak kok dizin",
    )
    ap.add_argument(
        "--out",
        default=r"C:\Users\mete\Downloads\UXMC\ucma\_forensic\strongest2_src\reports\DOWNLOADS_BAS_BI_ENVANTER.csv",
        help="CSV cikti yolu",
    )
    ap.add_argument(
        "--repo-root",
        default=r"C:\Users\mete\Downloads\UXMC\ucma\_forensic\strongest2_src",
        help="Mevcut stage20 aracinin bulundugu repo koku",
    )
    args = ap.parse_args(argv)

    scan_root = Path(args.scan_root).resolve()
    out_csv = Path(args.out).resolve()
    repo_root = Path(args.repo_root).resolve()

    rows = build_rows(scan_root)
    fields = [
        "full_path",
        "relative_path",
        "folder",
        "extension",
        "size_bytes",
        "created_at",
        "modified_at",
        "line_count",
        "include_count",
        "declare_count",
        "type_count",
        "function_count",
        "sub_count",
        "const_count",
        "first_nonempty",
        "content_info",
    ]

    write_csv_fn = load_stage20_writer(repo_root)
    if write_csv_fn is not None:
        write_csv_fn(out_csv, rows, fields)
        writer_name = "stage20.write_csv"
    else:
        write_csv_fallback(out_csv, rows, fields)
        writer_name = "csv.DictWriter(fallback)"

    print(f"[ENVANTER] dosya_sayisi={len(rows)}")
    print(f"[ENVANTER] csv={out_csv}")
    print(f"[ENVANTER] writer={writer_name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
