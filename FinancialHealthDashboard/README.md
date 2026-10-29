# Financial Health Dashboard

## Objective
Analyze income-statement performance, balance-sheet position, cash-flow movements, profitability and budget variance.

## Data files
- financial_data.csv: original small departmental sample retained for reference.
- income_statement_data.csv: 18 monthly synthetic income-statement periods from Jan 2025 to Jun 2026.
- balance_sheet_data.csv: monthly synthetic assets, liabilities and equity.
- cash_flow_data.csv: monthly operating, investing and financing cash flows.
- DAX_Measures.dax: reference measures.
- dashboard_layout.md: suggested pages.
- dashboard.html, balance_sheet.html and cash_flow.html: supplementary browser previews.

## PBIP source
Open ../PowerBIProjects/FinancialHealth/FinancialHealth.pbip in a recent Power BI Desktop version. Dataset content is embedded in the Power Query M partitions to avoid local source paths.

## Report pages
1. Executive Overview: revenue, net profit, margin, closing cash, revenue/profit trends, actual vs budget.
2. Balance Sheet & Cash Flow: assets vs liabilities, cash-flow trend, reconciliation detail.
3. Recommended extension: expense analysis and budget variance by month/category.

## Structural validation
- NetIncome = Revenue - TotalExpenses.
- BalanceCheck = TotalAssets - TotalLiabilitiesAndEquity = 0.
- NetCashFlow = OperatingCashFlow + InvestingCashFlow + FinancingCashFlow.
- ClosingCash = OpeningCash + NetCashFlow.

## Caveats
All figures are synthetic. This simplified income statement and illustrative balance sheet are not audited. No source transactions are available to reconcile to a general ledger. Validate all PBIP model measures/visuals in Power BI Desktop, then save a native PBIX file.
