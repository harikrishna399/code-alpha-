# Publish browser previews with GitHub Pages

1. Open this repository's Settings → Pages.
2. Under Build and deployment, choose Deploy from a branch.
3. Select main and /(root), then save.
4. When GitHub Pages shows the live URL, open the links on the portfolio homepage.
5. Pages containing relative CSV requests need to be served using HTTP(S); opening a local HTML file may block the data requests.

Previews include:
- index.html
- FinancialHealthDashboard/dashboard.html, balance_sheet.html, cash_flow.html
- HRAnalytics/dashboard.html, hiring_forecast.html
- RealEstateMarketTrends/dashboard.html, geographic_hotspots.html
- EducationalPerformance/dashboard.html, resource_allocation.html

If Pages is not enabled in repository settings, the interactive previews are not hosted even though their source files remain public.
