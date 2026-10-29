# Financial Health Dashboard

## Objective
Analyze revenue, expenses, profitability, cash position, and budget variance over time.

## Files
- `financial_data.csv`: synthetic monthly sample data for Jan 2025–Jun 2026.
- `DAX_Measures.dax`: starter measures for KPIs and budget variance.

## Import and model
1. Power BI Desktop → **Get data → Text/CSV** → select `financial_data.csv`.
2. Confirm `Date` is Date type and financial columns are Whole Number or Decimal Number.
3. Rename the imported table to `financial_data` (or update DAX names to match your table).
4. Create a Date table using **Modeling → New table**:

```dax
Date = CALENDAR(MIN(financial_data[Date]), MAX(financial_data[Date]))
```

5. Add a relationship from `Date[Date]` to `financial_data[Date]` and mark the Date table as a date table.

## Suggested report pages
### Page 1 — Executive Overview
- KPI cards: Total Revenue, Total Expenses, Net Profit, Profit Margin %.
- Line chart: Revenue and Net Profit by month.
- Clustered column chart: Actual Revenue vs Revenue Budget.
- Bar chart: Net Profit by Department.
- Slicers: Date, Department.

### Page 2 — Cost & Budget Analysis
- Actual vs budget expenses by month.
- Expense breakdown by Operating Expenses and Other Expenses.
- Variance cards and a table by month/department.

### Page 3 — Cash Position
- Opening and closing cash trend.
- Table showing each month's opening and closing cash.

## Business questions
- Is revenue growing over time?
- Which departments contribute most revenue?
- Are expenses above budget?
- Is profit margin improving or declining?

## Data limitations
This is sample data, not audited financial information. The current dataset is monthly and department-level. It does not contain a full balance sheet or transaction-level cash flow, so do not label the current report as a complete statutory financial statement. For a real balance sheet/cash-flow report, add assets, liabilities, equity, cash receipts, and cash payments at suitable levels of detail.

## Validation checklist
- Verify totals against the CSV.
- Check date sorting and data types.
- Confirm slicers filter every intended visual.
- Format currency consistently.
- Test zero/blank values in percentage measures.
- Save the finished report as `FinancialHealthDashboard.pbix` in this folder.