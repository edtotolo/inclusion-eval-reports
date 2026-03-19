"""
Publish an HTML eval report to GitHub Pages.

Usage:
  python publish.py --input ../outputs/eval_20260319.json
  python publish.py --input ../outputs/eval_20260319.json --name "haiku_baseline"

This script:
  1. Generates the HTML report from the JSON
  2. Copies it to ../docs/ (served by GitHub Pages)
  3. Updates ../docs/index.html with a link to the new report
  4. Commits and pushes to GitHub

First-time setup:
  git init (in the Inclusion Eval folder)
  git remote add origin https://github.com/YOUR_USERNAME/inclusion-eval-reports.git
  git checkout -b main
  Enable GitHub Pages on the repo: Settings > Pages > Source: main branch, /docs folder
"""

import subprocess
import sys
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime

EVAL_ROOT = Path(__file__).parent.parent
DOCS_DIR = EVAL_ROOT / "docs"

sys.path.insert(0, str(Path(__file__).parent))
from report_html import build_html


def update_index(reports: list[dict]) -> str:
    """Rebuild the docs/index.html listing page."""
    rows = ""
    for r in sorted(reports, key=lambda x: x.get("date", ""), reverse=True):
        label = r.get("label", "Unnamed")
        date = r.get("date", "")[:10]
        composite = r.get("composite", "N/A")
        flags = r.get("red_flags", 0)
        filename = r.get("filename", "")
        verdict = r.get("verdict", "")

        if verdict == "pass":
            badge = '<span style="background:#dcfce7;color:#166534;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:700">PASS</span>'
        elif verdict == "conditional":
            badge = '<span style="background:#fef9c3;color:#854d0e;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:700">CONDITIONAL</span>'
        else:
            badge = '<span style="background:#fee2e2;color:#991b1b;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:700">FAIL</span>'

        rows += f"""
        <tr>
          <td>{date}</td>
          <td><a href="{filename}">{label}</a></td>
          <td style="text-align:center">{composite}/100</td>
          <td style="text-align:center">{flags}</td>
          <td>{badge}</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Inclusion Eval — Reports</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 24px; color: #1e293b; }}
  h1 {{ font-size: 22px; font-weight: 700; margin-bottom: 4px; }}
  .subtitle {{ color: #64748b; margin-bottom: 32px; font-size: 14px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
  th {{ text-align: left; padding: 10px 12px; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; border-bottom: 2px solid #e2e8f0; }}
  td {{ padding: 12px 12px; border-bottom: 1px solid #f1f5f9; vertical-align: middle; }}
  tr:hover td {{ background: #f8fafc; }}
  a {{ color: #2563eb; text-decoration: none; font-weight: 500; }}
  a:hover {{ text-decoration: underline; }}
</style>
</head>
<body>
<h1>Financial Inclusion &amp; Consumer Protection AI Evaluations</h1>
<p class="subtitle">Assessment reports — click any row to view the full interactive report.</p>
<table>
  <thead>
    <tr>
      <th>Date</th>
      <th>AI Application</th>
      <th style="text-align:center">Score</th>
      <th style="text-align:center">Red flags</th>
      <th>Verdict</th>
    </tr>
  </thead>
  <tbody>
    {rows}
  </tbody>
</table>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="Publish eval report to GitHub Pages")
    parser.add_argument("--input", required=True, help="Input JSON eval result file")
    parser.add_argument("--name", default=None, help="Short name for the report file (default: derived from input filename)")
    parser.add_argument("--no-push", action="store_true", help="Generate files but do not git push")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = Path(__file__).parent / input_path

    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)

    # Generate HTML
    print("Generating HTML report...")
    html = build_html(data)

    # Determine output filename
    name = args.name or input_path.stem
    report_filename = f"{name}_report.html"

    # Write to docs/
    DOCS_DIR.mkdir(exist_ok=True)
    report_path = DOCS_DIR / report_filename
    report_path.write_text(html, encoding="utf-8")
    print(f"Report written: {report_path}")

    # Load or create registry
    registry_path = DOCS_DIR / "registry.json"
    if registry_path.exists():
        with open(registry_path) as f:
            registry = json.load(f)
    else:
        registry = []

    # Update registry
    meta = data.get("metadata", {})
    summary = data.get("summary", {})
    composite = summary.get("composite_score", 0)
    red_flag_count = len(summary.get("red_flags", []))

    if composite >= 75 and red_flag_count == 0:
        verdict = "pass"
    elif composite >= 55 and red_flag_count <= 1:
        verdict = "conditional"
    else:
        verdict = "fail"

    # Replace existing entry for same filename if present
    registry = [r for r in registry if r.get("filename") != report_filename]
    registry.append({
        "label": meta.get("label", "Unnamed"),
        "date": meta.get("timestamp", datetime.now().isoformat()),
        "composite": composite,
        "red_flags": red_flag_count,
        "verdict": verdict,
        "filename": report_filename,
    })

    with open(registry_path, "w") as f:
        json.dump(registry, f, indent=2)

    # Rebuild index
    index_html = update_index(registry)
    (DOCS_DIR / "index.html").write_text(index_html, encoding="utf-8")
    print("Index page updated.")

    if args.no_push:
        print("--no-push: skipping git commit and push.")
        return

    # Git commit and push
    repo_root = EVAL_ROOT
    try:
        subprocess.run(["git", "add", "docs/"], cwd=repo_root, check=True)
        subprocess.run(
            ["git", "commit", "-m", f"Add eval report: {meta.get('label', name)} ({datetime.now().strftime('%Y-%m-%d')})"],
            cwd=repo_root,
            check=True,
        )
        subprocess.run(["git", "push"], cwd=repo_root, check=True)
        print("\nPushed to GitHub. Report will be live at your GitHub Pages URL shortly.")
    except subprocess.CalledProcessError as e:
        print(f"\nGit error: {e}")
        print("Files are ready in docs/ — commit and push manually.")


if __name__ == "__main__":
    main()
