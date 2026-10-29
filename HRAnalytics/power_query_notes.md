# Power Query preparation — HR Analytics

1. Import `hr_employee_data.csv` from Text/CSV.
2. Set HireDate and ExitDate to Date type.
3. Treat blank ExitDate as null, not as a fabricated date.
4. Set PerformanceRating as Whole Number; SatisfactionScore as Decimal Number.
5. Standardize spelling/capitalization for Department, Location, JobRole, RecruitmentSource, and EmploymentStatus.
6. Check EmployeeID uniqueness.
7. For formal monthly turnover, add a monthly headcount snapshot and exits by month; do not calculate turnover using a single current employee list alone.

## Privacy checks
Remove direct identifiers from public dashboards. Prefer aggregated department/role-level visuals and restrict row-level employee details to authorized HR staff.