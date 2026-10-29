#!/usr/bin/env python3
"""Validate the synthetic CSV datasets used by the CodeAlpha project kits.

Run from the repository root: python scripts/validate_data.py
Uses only Python's standard library. This checks structure and simple data rules;
it does not validate business accuracy or make sample data production-ready.
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPECS = {
    "FinancialHealthDashboard/financial_data.csv": {
        "required": ["Date", "Department", "Revenue", "OperatingExpenses", "OtherExpenses", "OpeningCash", "ClosingCash", "BudgetRevenue", "BudgetExpenses"],
        "numeric": ["Revenue", "OperatingExpenses", "OtherExpenses", "OpeningCash", "ClosingCash", "BudgetRevenue", "BudgetExpenses"],
        "date": "Date",
    },
    "HRAnalytics/hr_employee_data.csv": {
        "required": ["EmployeeID", "Department", "JobRole", "Location", "HireDate", "ExitDate", "EmploymentStatus", "RecruitmentSource", "PerformanceRating", "SatisfactionScore", "TrainingHours", "MonthlySalary"],
        "numeric": ["PerformanceRating", "SatisfactionScore", "TrainingHours", "MonthlySalary"],
        "unique": ["EmployeeID"],
        "date": "HireDate",
    },
    "RealEstateMarketTrends/property_market_data.csv": {
        "required": ["Month", "City", "Neighborhood", "PropertyType", "AverageSalePrice", "AverageMonthlyRent", "Listings", "Transactions", "PopulationIndex", "PolicyRatePct"],
        "numeric": ["AverageSalePrice", "AverageMonthlyRent", "Listings", "Transactions", "PopulationIndex", "PolicyRatePct"],
        "date": "Month",
    },
    "EducationalPerformance/student_performance.csv": {
        "required": ["StudentID", "AcademicYear", "Term", "Department", "YearOfStudy", "AttendancePct", "MathScore", "ProgrammingScore", "CommunicationScore", "CreditsAttempted", "CreditsEarned", "LibraryVisits", "LabHours", "SupportFlag"],
        "numeric": ["AcademicYear", "Term", "YearOfStudy", "AttendancePct", "MathScore", "ProgrammingScore", "CommunicationScore", "CreditsAttempted", "CreditsEarned", "LibraryVisits", "LabHours"],
        "unique": ["StudentID"],
    },
}

def validate(path, spec):
    errors = []
    full = ROOT / path
    if not full.exists():
        return 0, [f"FILE MISSING: {path}"]
    with full.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        missing = [h for h in spec["required"] if h not in headers]
        if missing:
            errors.append("Missing required columns: " + ", ".join(missing))
        rows = list(reader)
    if not rows:
        errors.append("Dataset has no data rows")
    for col in spec.get("numeric", []):
        if col not in (headers or []):
            continue
        for line, row in enumerate(rows, start=2):
            value = row.get(col, "").strip()
            try:
                n = float(value)
                if not (n == n and abs(n) != float("inf")):
                    raise ValueError
            except (TypeError, ValueError):
                errors.append(f"Line {line}: {col} is not a finite number: {value!r}")
    for col in spec.get("unique", []):
        if col not in (headers or []):
            continue
        values = [r.get(col, "").strip() for r in rows]
        duplicates = sorted({v for v in values if v and values.count(v) > 1})
        if duplicates:
            errors.append(f"{col} contains duplicate values: {', '.join(duplicates[:10])}")
    date_col = spec.get("date")
    if date_col and date_col in (headers or []):
        from datetime import date
        for line, row in enumerate(rows, start=2):
            value = row.get(date_col, "").strip()
            try:
                date.fromisoformat(value)
            except ValueError:
                errors.append(f"Line {line}: invalid {date_col} ISO date: {value!r}")
    if "AttendancePct" in (headers or []):
        for line, row in enumerate(rows, start=2):
            try:
                n = float(row["AttendancePct"])
                if not 0 <= n <= 100:
                    errors.append(f"Line {line}: AttendancePct outside 0–100")
            except ValueError:
                pass
    for col in ("MathScore", "ProgrammingScore", "CommunicationScore", "PerformanceRating", "SatisfactionScore"):
        if col not in (headers or []):
            continue
        upper = 5 if col in ("PerformanceRating", "SatisfactionScore") else 100
        for line, row in enumerate(rows, start=2):
            try:
                n = float(row[col])
                if not 0 <= n <= upper:
                    errors.append(f"Line {line}: {col} outside expected 0–{upper} range")
            except ValueError:
                pass
    return len(rows), errors

def main():
    failed = False
    print("CodeAlpha CSV structural validation")
    print("=" * 38)
    for path, spec in SPECS.items():
        count, errors = validate(path, spec)
        status = "PASS" if not errors else "FAIL"
        print(f"{status}: {path} ({count} data rows)")
        for err in errors:
            print(f"  - {err}")
        failed |= bool(errors)
    print("\nNote: structural checks do not prove that synthetic data is factual or suitable for decisions.")
    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main())
