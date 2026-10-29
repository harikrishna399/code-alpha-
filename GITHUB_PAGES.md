# Viewing the browser previews with GitHub Pages

The HTML dashboards load their CSV files using browser fetch, so they should be served from a website rather than opened as local file URLs.

1. Open the repository Settings → Pages.
2. Under Build and deployment, select Deploy from a branch.
3. Select branch main and folder /(root), then save.
4. Wait for GitHub Pages to publish the site.
5. Visit the URLs shown by GitHub Pages:
   - /FinancialHealthDashboard/dashboard.html
   - /HRAnalytics/dashboard.html
   - /RealEstateMarketTrends/dashboard.html
   - /EducationalPerformance/dashboard.html

If Pages is not enabled, the source files can still be reviewed directly in GitHub, but the interactive previews may not run from the source-code view.
