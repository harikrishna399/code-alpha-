# Data dictionary and analytical assumptions

All CSV files are synthetic demonstration data, not records from an actual company, institution, property listing, employee, or student.

## Financial health
- income_statement_data.csv: 18 monthly periods (Jan 2025–Jun 2026) with revenue, cost of goods sold, operating and other expenses, depreciation, interest, tax, total expenses, net income and budget values.
- balance_sheet_data.csv: monthly cash, receivables, inventory, property/plant/equipment, payables, debt, total assets, total liabilities and equity.
- cash_flow_data.csv: operating, investing and financing cash flows, opening cash, net cash flow and closing cash.
- Arithmetic checks: NetIncome = Revenue − TotalExpenses; TotalAssets = TotalLiabilities + ShareholdersEquity; NetCashFlow = Operating + Investing + Financing; ClosingCash = OpeningCash + NetCashFlow.
- Figures are illustrative and not audited or statutory financial reporting.

## HR analytics
- hr_employee_data.csv: small synthetic employee-level sample.
- hr_monthly_metrics.csv: 24 months of department-level actual history (2024–2025) plus six months of projected planning scenario (Jan–Jun 2026).
- TurnoverRatePct on actual rows = exits / average opening and closing headcount × 100.
- ForecastHires is a basic planning scenario to approach planned headcount after estimated exits; it is not a trained or validated prediction model.

## Real estate
- property_market_data.csv: 12 months × 6 neighborhoods = 72 observations. Includes sale price, monthly rent, listings, transactions, population index, policy-rate context and approximate coordinates.
- Gross rental yield = monthly rent × 12 / sale price. It excludes vacancy, transaction costs, taxes, financing and maintenance.
- Demand-to-supply ratio = transactions / listings.
- Coordinates are approximate neighborhood centers; all financial and market values are synthetic, not real-time market data.

## Education
- student_performance.csv: synthetic student scores, attendance, credits, support flag and resource-use fields.
- resource_allocation.csv: synthetic department/term student counts, faculty, capacity/use metrics, tutor-hours gap, support counts and resource-gap score.
- Lab utilization = lab hours used / lab capacity hours.
- Library utilization uses a synthetic visit-capacity proxy, not actual occupancy.
- ResourceGapScore is a basic illustrative prioritization indicator, not a validated institutional index.

## PBIP project source
PowerBIProjects contains four source projects. Their TMDL partitions embed CSV text with Power Query M Base64 decoding so the data do not rely on a user-specific file path. The source projects still need Power BI Desktop open/refresh/render validation and native PBIX export.
