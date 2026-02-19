"""
Bulk-fix contrast / readability issues across all analysis notebooks.
Run once, then delete this file.

Replacements:
1. COLORS['muted'] '#95A5A6' → '#5D6D7E'  (WCAG AA compliant)
2. add_source_note fontsize=8 → fontsize=10
3. KPI label color '#7f8c8d' → '#4a5568'
4. grid alpha=0.3 → alpha=0.45  (except Venn-diagram circles)
5. HTML span color:#95A5A6 → color:#5D6D7E
6. NB05 HTML 'color: #f1f1f1' → 'color: #FFFFFF'
7. fontsize=8 (various) → fontsize=10
8. Tick color rcParams using COLORS['muted'] → '#5D6D7E' (already handled by #1)
"""

import json, re, sys, os

NOTEBOOKS = [
    "notebooks/00_executive_summary.ipynb",
    "notebooks/01_data_import_and_checks.ipynb",
    "notebooks/02_descriptive_analysis.ipynb",
    "notebooks/03_barriers_analysis.ipynb",
    "notebooks/04_from_barriers_to_policy.ipynb",
    "notebooks/05_predictive_analytics.ipynb",
]

BASE = os.path.dirname(os.path.abspath(__file__))


def fix_notebook(rel_path):
    path = os.path.join(BASE, rel_path)
    if not os.path.exists(path):
        print(f"  SKIP (not found): {rel_path}")
        return 0

    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()

    original = raw
    count = 0

    # 1. COLORS dict: '#95A5A6' → '#5D6D7E'
    n = raw.count("'#95A5A6'")
    if n:
        raw = raw.replace("'#95A5A6'", "'#5D6D7E'")
        count += n
        print(f"    [1] COLORS muted '#95A5A6' → '#5D6D7E': {n} hits")

    # Also handle in HTML output cells and source where it's unquoted or in CSS
    n = raw.count("#95A5A6")
    if n:
        raw = raw.replace("#95A5A6", "#5D6D7E")
        count += n
        print(f"    [1b] HTML #95A5A6 → #5D6D7E: {n} hits")

    # 2. add_source_note fontsize: fontsize=8 in the specific pattern
    old = "fontsize=8, color=COLORS['muted']"
    new = "fontsize=10, color=COLORS['muted']"
    n = raw.count(old)
    if n:
        raw = raw.replace(old, new)
        count += n
        print(f"    [2] add_source_note fontsize 8→10: {n} hits")

    # 3. KPI label color: #7f8c8d → #4a5568
    n = raw.count("#7f8c8d")
    if n:
        raw = raw.replace("#7f8c8d", "#4a5568")
        count += n
        print(f"    [3] KPI label #7f8c8d → #4a5568: {n} hits")

    # 4. Grid alpha=0.3 → alpha=0.45
    #    Match grid(alpha=0.3) and grid(axis='...', alpha=0.3) patterns
    #    But NOT fill=True patterns (Venn diagram circles)
    old_grid = "alpha=0.3)"
    # We need to be careful: only replace in grid() calls, not in MCircle / fill calls
    # Strategy: replace "grid(alpha=0.3)" and "grid(axis='...', alpha=0.3)"
    patterns = [
        ("grid(alpha=0.3)", "grid(alpha=0.45)"),
        ("grid(axis='x', alpha=0.3)", "grid(axis='x', alpha=0.45)"),
        ("grid(axis='y', alpha=0.3)", "grid(axis='y', alpha=0.45)"),
    ]
    for old_p, new_p in patterns:
        n = raw.count(old_p)
        if n:
            raw = raw.replace(old_p, new_p)
            count += n
            print(f"    [4] {old_p} → {new_p}: {n} hits")

    # 5. NB05: color: #f1f1f1 → color: #FFFFFF  (white text on dark bg headers)
    old_f1 = "color: #f1f1f1"
    new_f1 = "color: #FFFFFF"
    n = raw.count(old_f1)
    if n:
        raw = raw.replace(old_f1, new_f1)
        count += n
        print(f"    [5] HTML '#f1f1f1' → '#FFFFFF': {n} hits")

    # 6. Remaining fontsize=8 in source cells (e.g. threshold labels, tick labels)
    #    Pattern: fontsize=8 that's NOT already been replaced
    #    Be selective: replace fontsize=8 with fontsize=10 in text annotations
    remaining_fs8 = raw.count("fontsize=8")
    if remaining_fs8:
        raw = raw.replace("fontsize=8", "fontsize=10")
        count += remaining_fs8
        print(f"    [6] fontsize=8 → fontsize=10: {remaining_fs8} hits")

    # 7. font-size:11px in KPI labels → font-size:12px for better readability
    #    (these are the small grey labels under KPI values)
    old_fs11 = "font-size:11px"
    new_fs11 = "font-size:12px"
    n = raw.count(old_fs11)
    if n:
        raw = raw.replace(old_fs11, new_fs11)
        count += n
        print(f"    [7] font-size:11px → font-size:12px: {n} hits")

    if raw != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(raw)
        print(f"  ✅ {rel_path}: {count} replacements written")
    else:
        print(f"  ⚪ {rel_path}: no changes needed")

    return count


if __name__ == "__main__":
    total = 0
    for nb in NOTEBOOKS:
        print(f"\n📓 {nb}")
        total += fix_notebook(nb)
    print(f"\n{'='*50}")
    print(f"Total replacements: {total}")
