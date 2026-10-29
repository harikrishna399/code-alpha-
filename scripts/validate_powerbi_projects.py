#!/usr/bin/env python3
"""Validate project JSON/TMDL paths, embedded CSVs, tables, relationships and visuals."""
import base64
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = {
    "FinancialHealth": {"tables":{"income_statement_data","balance_sheet_data","cash_flow_data","DateTable"}, "pages":2},
    "HRAnalytics": {"tables":{"hr_monthly_metrics","hr_employee_data","DateTable"}, "pages":2},
    "RealEstateMarket": {"tables":{"property_market_data","DateTable"}, "pages":2},
    "EducationPerformance": {"tables":{"student_performance","resource_allocation","DepartmentTable"}, "pages":2},
}

def check(condition, message):
    if not condition:
        raise AssertionError(message)

def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise AssertionError("Invalid JSON " + str(path.relative_to(ROOT)) + ": " + str(exc))

def validate_table(path, table_name):
    body = path.read_text(encoding="utf-8")
    check(body.startswith("table " + table_name + "\n"), str(path) + ": table declaration mismatch")
    check("partition " + table_name + " = m" in body, str(path) + ": missing M partition")
    match = re.search(r'Binary\.FromText\("([A-Za-z0-9+/=]+)", BinaryEncoding\.Base64\)', body)
    check(match is not None, str(path) + ": missing embedded CSV")
    raw = base64.b64decode(match.group(1)).decode("utf-8")
    header = next(csv.reader([raw.splitlines()[0]]))
    declared = re.findall(r"^\s*column ([A-Za-z0-9_]+)\s*$", body, flags=re.M)
    check(header == declared, str(path) + ": embedded CSV header does not match TMDL column declarations")
    check("Table.TransformColumnTypes" in body, str(path) + ": missing type conversion")
    return header

def validate_project(slug, spec):
    root = ROOT / "PowerBIProjects" / slug
    pbip = read_json(root / (slug + ".pbip"))
    report_name = slug + ".Report"
    model_name = slug + ".SemanticModel"
    check(pbip.get("artifacts", [{}])[0].get("report", {}).get("path") == report_name, slug + ": wrong report path")
    report_root, model_root = root / report_name, root / model_name
    pbir = read_json(report_root / "definition.pbir")
    check(pbir.get("datasetReference", {}).get("byPath", {}).get("path") == "../" + model_name, slug + ": wrong model reference")
    read_json(model_root / "definition.pbism")
    read_json(report_root / "definition/version.json")
    read_json(report_root / "definition/report.json")
    model = (model_root / "definition/model.tmdl").read_text(encoding="utf-8")
    declared_tables = set(re.findall(r"^ref table ([A-Za-z0-9_]+)$", model, flags=re.M))
    check(spec["tables"] <= declared_tables, slug + ": missing model table refs " + repr(spec["tables"] - declared_tables))
    table_paths = list((model_root / "definition/tables").glob("*.tmdl"))
    check(len(table_paths) >= len(spec["tables"]), slug + ": missing TMDL table files")
    for path in table_paths:
        validate_table(path, path.stem)
    rel = model_root / "definition/relationships.tmdl"
    if rel.exists():
        rel_body = rel.read_text(encoding="utf-8")
        for table_name in re.findall(r"(?:fromColumn|toColumn): ([A-Za-z0-9_]+)\.", rel_body):
            check(table_name in declared_tables, slug + ": relationship references unknown table " + table_name)
    pages_path = report_root / "definition/pages/pages.json"
    pages_meta = read_json(pages_path)
    page_ids = pages_meta.get("pageOrder", [])
    check(len(page_ids) == spec["pages"], slug + ": expected " + str(spec["pages"]) + " report pages")
    visuals = 0
    for page_id in page_ids:
        page_dir = report_root / "definition/pages" / page_id
        page = read_json(page_dir / "page.json")
        check(page.get("name") == page_id, slug + ": page name differs from its folder")
        for visual_path in (page_dir / "visuals").glob("*/visual.json"):
            visual = read_json(visual_path)
            check("visualType" in visual.get("visual", {}), str(visual_path) + ": missing visualType")
            query = visual.get("visual", {}).get("query", {}).get("queryState", {})
            for role in query.values():
                for projection in role.get("projections", []):
                    field = projection.get("field", {})
                    ref = None
                    if "Column" in field:
                        ref = field["Column"].get("Expression", {}).get("SourceRef", {}).get("Entity")
                    elif "Measure" in field:
                        ref = field["Measure"].get("Expression", {}).get("SourceRef", {}).get("Entity")
                    elif "Aggregation" in field:
                        ref = field["Aggregation"].get("Expression", {}).get("Column", {}).get("Expression", {}).get("SourceRef", {}).get("Entity")
                    if ref:
                        check(ref in declared_tables, str(visual_path) + ": unknown query table " + str(ref))
            visuals += 1
    check(visuals >= 8, slug + ": expected at least 8 visuals")
    return len(table_paths), len(page_ids), visuals

def main():
    total_visuals = 0
    for slug, spec in PROJECTS.items():
        table_count, page_count, visual_count = validate_project(slug, spec)
        total_visuals += visual_count
        print("PASS " + slug + ": " + str(table_count) + " tables, " + str(page_count) + " pages, " + str(visual_count) + " visuals")
    print("PBIP source checks passed for all four projects; total visuals: " + str(total_visuals))
    print("Desktop open/refresh/render validation is still required.")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError as exc:
        print("FAIL: " + str(exc), file=sys.stderr)
        sys.exit(1)
