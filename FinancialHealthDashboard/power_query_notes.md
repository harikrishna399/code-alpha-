# Power Query preparation — Financial Health

1. Import `financial_data.csv` from Text/CSV.
2. Set `Date` to Date; set revenue, expenses, cash, and budget columns to Decimal Number or Whole Number.
3. Trim and clean `Department`.
4. Check that there are no duplicate Date + Department combinations unless intentionally expected.
5. If the dataset is expanded, use a separate transaction table for revenue/expense detail and a separate cash-flow table for receipts/payments.
6. Close & Apply, then create the measures listed in `DAX_Measures.dax`.

## Suggested quality checks
- Revenue, expenses, and budgets should not be null.
- Confirm date parsing uses the correct locale.
- Keep a clear distinction between operating profit and net profit if taxes, interest, and non-operating items are later added.