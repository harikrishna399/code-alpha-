# Human Resources Analytics

## Objective
Analyze recruitment funnel, exits, turnover, satisfaction, performance, training and hiring needs.

## Data files
- hr_employee_data.csv: 20 synthetic employee sample records.
- hr_monthly_metrics.csv: 24 months of synthetic actual monthly data for five departments plus six months of 2026 scenario rows.
- DAX_Measures.dax: reference measures.
- dashboard_layout.md: suggested report pages.
- dashboard.html and hiring_forecast.html: supplementary browser previews.

## PBIP source
Open ../PowerBIProjects/HRAnalytics/HRAnalytics.pbip in Power BI Desktop.

## Report pages
1. Workforce Overview: hires/exits, turnover, recruitment funnel, satisfaction/performance.
2. Recruitment & Hiring Scenario: projected hiring needs, applications/offers, time-to-fill and employee sample.

## Definitions and limits
Monthly turnover is exits / average opening and closing headcount. ForecastHires is an illustrative scenario that approaches the planned headcount after estimated exits. It is not a fitted predictive model. A defensible forecast needs validated historical headcounts, requisition/applicant funnel, time-to-fill, hiring plans and seasonality. Filter RecordType when comparing actual and forecast periods.
All data are synthetic; protect personal data in real HR reports. Validate the Power BI source in Desktop and save a PBIX when successful.
