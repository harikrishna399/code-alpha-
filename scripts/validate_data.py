#!/usr/bin/env python3
"""Validate CSV structure, ranges and cross-file financial/HR arithmetic."""
import csv
import math
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(rel):
    path = ROOT / rel
    if not path.exists():
        raise AssertionError("Missing file: " + rel)
    with path.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        headers = reader.fieldnames or []
        rows = list(reader)
    if not headers or not rows:
        raise AssertionError(rel + ": missing header or data rows")
    return headers, rows

def require_columns(rel, headers, required):
    missing = sorted(set(required) - set(headers))
    if missing:
        raise AssertionError(rel + ": missing columns " + ", ".join(missing))

def num(row, col, rel, allow_blank=False):
    value = (row.get(col) or "").strip()
    if allow_blank and not value:
        return None
    try:
        out = float(value)
    except (ValueError, TypeError):
        raise AssertionError(rel + ": invalid numeric value for " + col + ": " + repr(value))
    if not math.isfinite(out):
        raise AssertionError(rel + ": non-finite numeric value for " + col)
    return out

def date_value(value, rel, field, allow_blank=False):
    value = (value or "").strip()
    if allow_blank and not value:
        return
    try:
        date.fromisoformat(value)
    except ValueError:
        raise AssertionError(rel + ": invalid ISO date in " + field + ": " + repr(value))

def check(rel, required, numeric=(), dates=(), unique=(), optional_numeric=()):
    headers, rows = load(rel)
    require_columns(rel, headers, required)
    for i, row in enumerate(rows, start=2):
        for field in numeric:
            num(row, field, rel + ":" + str(i))
        for field in optional_numeric:
            num(row, field, rel + ":" + str(i), allow_blank=True)
        for field, blank_ok in dates:
            date_value(row.get(field), rel + ":" + str(i), field, blank_ok)
    for field in unique:
        values = [row.get(field, "") for row in rows]
        if len(values) != len(set(values)):
            raise AssertionError(rel + ": duplicate " + field)
    return rows

def close(a, b, message):
    if abs(a - b) > 1:
        raise AssertionError(message + " (difference " + str(a - b) + ")")

def main():
    results = []
    old_fin = check("FinancialHealthDashboard/financial_data.csv",
        ["Date","Department","Revenue","OperatingExpenses","OtherExpenses","OpeningCash","ClosingCash","BudgetRevenue","BudgetExpenses"],
        numeric=["Revenue","OperatingExpenses","OtherExpenses","OpeningCash","ClosingCash","BudgetRevenue","BudgetExpenses"], dates=[("Date", False)])
    income = check("FinancialHealthDashboard/income_statement_data.csv",
        ["Date","Revenue","CostOfGoodsSold","OperatingExpenses","OtherExpenses","Depreciation","InterestExpense","IncomeTax","TotalExpenses","NetIncome","BudgetRevenue","BudgetExpenses"],
        numeric=["Revenue","CostOfGoodsSold","OperatingExpenses","OtherExpenses","Depreciation","InterestExpense","IncomeTax","TotalExpenses","NetIncome","BudgetRevenue","BudgetExpenses"], dates=[("Date", False)])
    for i, row in enumerate(income, start=2):
        total = sum(num(row, f, "income_statement_data.csv") for f in ["CostOfGoodsSold","OperatingExpenses","OtherExpenses","Depreciation","InterestExpense","IncomeTax"])
        close(total, num(row, "TotalExpenses", "income_statement_data.csv"), "income_statement_data.csv row " + str(i) + ": expenses do not tie")
        close(num(row, "Revenue", "income_statement_data.csv") - total, num(row, "NetIncome", "income_statement_data.csv"), "income_statement_data.csv row " + str(i) + ": net income does not tie")
    bs = check("FinancialHealthDashboard/balance_sheet_data.csv",
        ["Date","Cash","AccountsReceivable","Inventory","PropertyPlantEquipment","TotalAssets","AccountsPayable","ShortTermDebt","LongTermDebt","TotalLiabilities","ShareholdersEquity","TotalLiabilitiesAndEquity","BalanceCheck"],
        numeric=["Cash","AccountsReceivable","Inventory","PropertyPlantEquipment","TotalAssets","AccountsPayable","ShortTermDebt","LongTermDebt","TotalLiabilities","ShareholdersEquity","TotalLiabilitiesAndEquity","BalanceCheck"], dates=[("Date", False)])
    for i, row in enumerate(bs, start=2):
        assets = sum(num(row,f,"balance_sheet_data.csv") for f in ["Cash","AccountsReceivable","Inventory","PropertyPlantEquipment"])
        liabilities = sum(num(row,f,"balance_sheet_data.csv") for f in ["AccountsPayable","ShortTermDebt","LongTermDebt"])
        close(assets, num(row,"TotalAssets","balance_sheet_data.csv"), "balance sheet assets do not tie on row " + str(i))
        close(liabilities, num(row,"TotalLiabilities","balance_sheet_data.csv"), "balance sheet liabilities do not tie on row " + str(i))
        close(assets, num(row,"TotalLiabilitiesAndEquity","balance_sheet_data.csv"), "balance sheet equation does not tie on row " + str(i))
        close(0, num(row,"BalanceCheck","balance_sheet_data.csv"), "balance check not zero on row " + str(i))
    cf = check("FinancialHealthDashboard/cash_flow_data.csv",
        ["Date","OpeningCash","OperatingCashFlow","InvestingCashFlow","FinancingCashFlow","NetCashFlow","ClosingCash"],
        numeric=["OpeningCash","OperatingCashFlow","InvestingCashFlow","FinancingCashFlow","NetCashFlow","ClosingCash"], dates=[("Date", False)])
    bs_by_date = {r["Date"]: r for r in bs}
    for i, row in enumerate(cf, start=2):
        net = sum(num(row,f,"cash_flow_data.csv") for f in ["OperatingCashFlow","InvestingCashFlow","FinancingCashFlow"])
        close(net, num(row,"NetCashFlow","cash_flow_data.csv"), "cash-flow net does not tie on row " + str(i))
        close(num(row,"OpeningCash","cash_flow_data.csv") + net, num(row,"ClosingCash","cash_flow_data.csv"), "cash roll-forward does not tie on row " + str(i))
        if row["Date"] in bs_by_date:
            close(num(row,"ClosingCash","cash_flow_data.csv"), num(bs_by_date[row["Date"]],"Cash","balance_sheet_data.csv"), "cash flow and balance-sheet cash mismatch on " + row["Date"])
    employees = check("HRAnalytics/hr_employee_data.csv",
        ["EmployeeID","Department","JobRole","Location","HireDate","ExitDate","EmploymentStatus","RecruitmentSource","PerformanceRating","SatisfactionScore","TrainingHours","MonthlySalary"],
        numeric=["PerformanceRating","SatisfactionScore","TrainingHours","MonthlySalary"], dates=[("HireDate",False),("ExitDate",True)], unique=["EmployeeID"])
    for i, row in enumerate(employees, start=2):
        for field in ["PerformanceRating","SatisfactionScore"]:
            value = num(row,field,"hr_employee_data.csv")
            if not 0 <= value <= 5:
                raise AssertionError("HR " + field + " outside 0–5 on row " + str(i))
    hr = check("HRAnalytics/hr_monthly_metrics.csv",
        ["Month","Department","RecordType","OpeningHeadcount","Hires","Exits","ClosingHeadcount","Applications","Offers","Requisitions","AverageTimeToFillDays","PlannedHeadcount","ForecastHires","TurnoverRatePct","SatisfactionScore","PerformanceRating","TrainingHours"],
        numeric=["OpeningHeadcount","Applications","Offers","Requisitions","AverageTimeToFillDays","PlannedHeadcount"],
        dates=[("Month",False)],
        optional_numeric=["Hires","Exits","ClosingHeadcount","ForecastHires","TurnoverRatePct","SatisfactionScore","PerformanceRating","TrainingHours"])
    actual = forecast = 0
    for i, row in enumerate(hr, start=2):
        if row["RecordType"] == "Actual":
            actual += 1
            close(num(row,"OpeningHeadcount","hr_monthly_metrics.csv") + num(row,"Hires","hr_monthly_metrics.csv") - num(row,"Exits","hr_monthly_metrics.csv"), num(row,"ClosingHeadcount","hr_monthly_metrics.csv"), "HR headcount arithmetic failed on row " + str(i))
            turnover = num(row,"TurnoverRatePct","hr_monthly_metrics.csv")
            if not 0 <= turnover <= 100:
                raise AssertionError("HR turnover outside 0–100 on row " + str(i))
        elif row["RecordType"] == "Scenario Forecast":
            forecast += 1
            if num(row,"ForecastHires","hr_monthly_metrics.csv") < 0:
                raise AssertionError("Negative forecast hiring need on row " + str(i))
        else:
            raise AssertionError("Unknown HR RecordType on row " + str(i))
    if not actual or not forecast:
        raise AssertionError("HR dataset must contain both actual and scenario forecast rows")
    real_estate = check("RealEstateMarketTrends/property_market_data.csv",
        ["Month","City","Neighborhood","PropertyType","AverageSalePrice","AverageMonthlyRent","Listings","Transactions","PopulationIndex","PolicyRatePct","Latitude","Longitude","RecordType"],
        numeric=["AverageSalePrice","AverageMonthlyRent","Listings","Transactions","PopulationIndex","PolicyRatePct","Latitude","Longitude"], dates=[("Month",False)])
    for i, row in enumerate(real_estate, start=2):
        if num(row,"AverageSalePrice","property_market_data.csv") <= 0 or num(row,"AverageMonthlyRent","property_market_data.csv") <= 0:
            raise AssertionError("Non-positive sale price/rent on row " + str(i))
        lat, lon = num(row,"Latitude","property_market_data.csv"), num(row,"Longitude","property_market_data.csv")
        if not -90 <= lat <= 90 or not -180 <= lon <= 180:
            raise AssertionError("Invalid coordinates on row " + str(i))
    students = check("EducationalPerformance/student_performance.csv",
        ["StudentID","AcademicYear","Term","Department","YearOfStudy","AttendancePct","MathScore","ProgrammingScore","CommunicationScore","CreditsAttempted","CreditsEarned","LibraryVisits","LabHours","SupportFlag"],
        numeric=["AcademicYear","Term","YearOfStudy","AttendancePct","MathScore","ProgrammingScore","CommunicationScore","CreditsAttempted","CreditsEarned","LibraryVisits","LabHours"], unique=["StudentID"])
    for i, row in enumerate(students, start=2):
        for field in ["AttendancePct","MathScore","ProgrammingScore","CommunicationScore"]:
            val=num(row,field,"student_performance.csv")
            if not 0 <= val <= 100:
                raise AssertionError(field + " outside 0–100 on row " + str(i))
        if num(row,"CreditsEarned","student_performance.csv") > num(row,"CreditsAttempted","student_performance.csv"):
            raise AssertionError("CreditsEarned exceeds attempted on row " + str(i))
    resources = check("EducationalPerformance/resource_allocation.csv",
        ["AcademicYear","Term","Department","StudentCount","FacultyCount","FacultyRecommended","LabCapacityHours","LabHoursUsed","LabUtilizationPct","LibraryVisits","LibraryVisitsCapacity","LibraryUtilizationPct","TutorHoursAvailable","TutorHoursRecommended","TutorHourGap","SupportFlagCount","ResourceGapScore"],
        numeric=["AcademicYear","Term","StudentCount","FacultyCount","FacultyRecommended","LabCapacityHours","LabHoursUsed","LabUtilizationPct","LibraryVisits","LibraryVisitsCapacity","LibraryUtilizationPct","TutorHoursAvailable","TutorHoursRecommended","TutorHourGap","SupportFlagCount","ResourceGapScore"])
    for i, row in enumerate(resources, start=2):
        if num(row,"TutorHourGap","resource_allocation.csv") < 0:
            raise AssertionError("Negative tutor-hours gap on row " + str(i))
        if num(row,"LabUtilizationPct","resource_allocation.csv") < 0:
            raise AssertionError("Negative lab utilization on row " + str(i))
    checks = [
        ("financial_data.csv", len(old_fin)), ("income_statement_data.csv", len(income)),
        ("balance_sheet_data.csv", len(bs)), ("cash_flow_data.csv", len(cf)),
        ("hr_employee_data.csv", len(employees)), ("hr_monthly_metrics.csv", len(hr)),
        ("property_market_data.csv", len(real_estate)), ("student_performance.csv", len(students)),
        ("resource_allocation.csv", len(resources))
    ]
    print("CodeAlpha dataset validation: PASS")
    for label, count in checks:
        print("  PASS " + label + ": " + str(count) + " rows")
    print("  PASS HR status split: " + str(actual) + " actual rows, " + str(forecast) + " scenario forecast rows")
    print("  PASS financial statement arithmetic and cash-flow roll-forward")
    print("Reminder: structural/arithmetic validation does not make synthetic data factual.")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError as exc:
        print("FAIL: " + str(exc), file=sys.stderr)
        sys.exit(1)
