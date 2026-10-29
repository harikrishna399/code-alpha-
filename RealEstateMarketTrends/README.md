# Real Estate Market Trends Dashboard

## Objective
Compare property sale prices, rent, estimated gross rental yield, listing supply, transaction demand, and regional trends.

## Files
- `property_market_data.csv`: synthetic monthly market sample for three cities and selected neighborhoods.
- `DAX_Measures.dax`: starter DAX measures.

## Build steps
1. Import the CSV using Power BI Desktop → Get data → Text/CSV.
2. Rename the table to `property_market_data`.
3. Set Month to Date; prices/rent to Currency; Listings/Transactions to Whole Number; PolicyRatePct to Decimal Number.
4. Create a Date table: `Date = CALENDAR(MIN(property_market_data[Month]), MAX(property_market_data[Month]))`.
5. Relate Date[Date] to property_market_data[Month] and mark the Date table as a date table.

## Report pages
### Market Overview
- KPI cards: Average Sale Price, Average Monthly Rent, Estimated Annual Rental Yield %.
- Line chart: Average Sale Price by Month.
- Column chart: Transactions and Listings by City.
- Slicers: City, Neighborhood, Property Type, Month.

### Yield & Affordability
- Bar chart: estimated rental yield by neighborhood.
- Scatter chart: Average Sale Price vs Average Monthly Rent.
- Table: city, neighborhood, price, rent, listings, transactions.

### Supply & Demand
- Demand-to-supply ratio by neighborhood.
- Monthly listings vs transactions.
- Map visual using City or neighborhood geographic fields if geocoding is reliable; verify locations manually.

## Analytical caveats
Data is synthetic and illustrates report construction only. Sale price and rent are neighborhood-level sample indicators, not verified current market quotes. Gross rental yield excludes vacancy, taxes, repairs, maintenance, and financing. Policy rate is contextual and should not be interpreted as causal evidence.

## Validation
- Confirm monthly rows sort chronologically.
- Format prices as INR (₹).
- Verify slicers filter all visuals.
- Use a map only after checking geocoding accuracy.
- Save as `RealEstateMarketTrends.pbix` in this folder.