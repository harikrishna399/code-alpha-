# CodeAlpha Power BI Analytics Portfolio

This repository contains all four project tracks from the supplied CodeAlpha Power BI brief. The PDF permits completing any **2 or 3 of 4 tasks**; all four tracks are prepared here.

## Project entry points

| Task | Supporting folder | Power BI Project source | Browser preview |
|---|---|---|---|
| 1. Financial Health Dashboard | [Financial folder](FinancialHealthDashboard/) | [Open PBIP](PowerBIProjects/FinancialHealth/FinancialHealth.pbip) | [Overview](FinancialHealthDashboard/dashboard.html) · [Balance sheet](FinancialHealthDashboard/balance_sheet.html) · [Cash flow](FinancialHealthDashboard/cash_flow.html) |
| 2. HR Analytics | [HR folder](HRAnalytics/) | [Open PBIP](PowerBIProjects/HRAnalytics/HRAnalytics.pbip) | [Overview](HRAnalytics/dashboard.html) · [Hiring scenario](HRAnalytics/hiring_forecast.html) |
| 3. Real Estate Market Trends | [Real-estate folder](RealEstateMarketTrends/) | [Open PBIP](PowerBIProjects/RealEstateMarket/RealEstateMarket.pbip) | [Overview](RealEstateMarketTrends/dashboard.html) · [Geographic hotspots](RealEstateMarketTrends/geographic_hotspots.html) |
| 4. Educational Performance and Resource Allocation | [Education folder](EducationalPerformance/) | [Open PBIP](PowerBIProjects/EducationPerformance/EducationPerformance.pbip) | [Academic overview](EducationalPerformance/dashboard.html) · [Resource allocation](EducationalPerformance/resource_allocation.html) |

The source projects use the Power BI Project (PBIP) format with a TMDL semantic model and PBIR report definitions. The dataset CSV is embedded in the model's Power Query M partitions to avoid machine-specific paths; the human-readable CSV files remain in this repository. Microsoft documents PBIP and PBIR as source-controlled Power BI project formats; see [Power BI project overview](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview) and [report folder/PBIR structure](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report).

## Open the Power BI projects

1. Clone or download this repository.
2. Open the corresponding .pbip file in a recent Power BI Desktop version.
3. Review compatibility notices, refresh/apply model changes if prompted, and inspect measures, report visuals, relationships and filters.
4. Save a native .pbix using **File → Save As** only after Desktop has successfully opened and validated the project.
5. Commit/push the .pbix file into the corresponding task folder and update PROJECT_STATUS.md.

**Important limitation:** this environment has no Power BI Desktop engine. The PBIP source files and report definitions have been pushed and JSON syntax checked, but they have not been opened/refreshed/rendered in Desktop here. Native PBIX creation and validation are therefore not claimed as complete.

## Validate locally

Run from the repository root:

    python scripts/validate_data.py
    python scripts/validate_powerbi_projects.py

A GitHub Actions workflow runs both checks on pushes and pull requests. These checks verify the data structure and PBIP file references; they do not replace opening and rendering the reports in Power BI Desktop.

## Data provenance and limitations

All data files are **synthetic demonstration data**. They are not real company finances, employee records, current property listings, or real student records.

- Finance includes separate income-statement, balance-sheet and cash-flow samples, but they are not audited statements.
- HR includes monthly sample history plus a six-month illustrative headcount scenario, not a statistically validated hiring prediction.
- Real-estate values are illustrative and not a live market feed. Coordinates indicate approximate neighborhood centers, not specific properties.
- Education results and resource utilization are synthetic and must not be used to make decisions about real students or staff.

See [DATA_DICTIONARY.md](DATA_DICTIONARY.md) and [PROJECT_STATUS.md](PROJECT_STATUS.md).

## PDF-required external steps

- Share your internship status on LinkedIn and tag @CodeAlpha.
- Publish a video explanation with the GitHub repository link.
- Submit the completed work through the submission form shared in your internship WhatsApp group.

The narration and recording checklist are in [LINKEDIN_DEMO_SCRIPT.md](LINKEDIN_DEMO_SCRIPT.md). The supplied PDF does not contain the submission form URL, so it must be obtained from the official WhatsApp group. No LinkedIn post, video upload, or form submission is claimed as completed.
