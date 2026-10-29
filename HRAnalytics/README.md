# Human Resources Analytics Dashboard

## Objective
Analyze workforce composition, recruitment sources, employee exits, performance, satisfaction, and training.

## Files
- `hr_employee_data.csv`: synthetic employee-level sample dataset.
- `DAX_Measures.dax`: starter measures for workforce KPIs.

## Import and prepare
1. Power BI Desktop → **Get data → Text/CSV** → select `hr_employee_data.csv`.
2. Rename the table to `hr_employee_data` or adjust the DAX table name.
3. Set `HireDate` and `ExitDate` to Date types; keep blank exit dates as null.
4. Set salary to Currency/Decimal and satisfaction to Decimal.
5. For a date analysis, create a Date table and relate it to HireDate. If analyzing ExitDate too, create an inactive relationship or a second role-playing date table.

## Suggested report pages
### Page 1 — Workforce Overview
- KPI cards: Total Employees, Active Employees, Exited Employees, Average Satisfaction.
- Bar chart: Active employees by Department.
- Donut chart: Employment Status.
- Slicers: Department, Location, Job Role.

### Page 2 — Recruitment & Attrition
- Hires by month/year and Recruitment Source.
- Exits by year and department.
- Table of exited employees for authorized HR users only.
- Clearly label the current exit share as a sample-data metric, not a formal turnover rate.

### Page 3 — Performance & Engagement
- Average Performance Rating by Department.
- Average Satisfaction by Department.
- Training Hours vs Performance Rating scatter chart.
- Salary distribution by role (avoid exposing individual compensation in public reports).

## Business questions
- Which recruitment sources appear most frequently in the sample?
- Which departments have the most listed exits?
- How do satisfaction and performance differ by department?
- Is training associated with higher performance in this small sample?

## Forecasting limitation
The brief asks for predictive hiring analytics. This starter dataset is too small and lacks monthly requisitions, applications, time-to-fill, planned headcount, and historical workforce snapshots. A credible hiring forecast should use those additional fields and a time-series or scenario model; do not present a forecast as validated from this sample alone.

## Privacy
All records are synthetic. For real HR data, restrict access, aggregate results where possible, and do not publish personally identifiable or sensitive employee information.

## Validation checklist
- Verify active/exited counts against the CSV.
- Check blanks in ExitDate are treated as null.
- Confirm date and department slicers work.
- Apply appropriate privacy permissions.
- Save the finished report as `HRAnalytics.pbix` in this folder.