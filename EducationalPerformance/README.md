# Educational Performance and Resource Allocation Dashboard

## Objective
Evaluate academic outcomes, attendance, credit completion, and learning-resource usage to support education management.

## Files
- `student_performance.csv`: synthetic student-term sample data.
- `DAX_Measures.dax`: starter measures for academic performance and resource indicators.

## Import and model
1. Import CSV with Power BI Desktop → Get data → Text/CSV.
2. Rename the table to `student_performance`.
3. Set numeric columns to Whole Number/Decimal; confirm percentages are stored from 0–100.
4. Treat AcademicYear and Term as categorical fields. If adding real dates, use a proper academic calendar dimension.
5. Keep StudentID out of public-facing visuals and apply access controls to detailed data.

## Report pages
### Page 1 — Academic Overview
- KPI cards: Student Count, Average Attendance %, Average Overall Score, Credit Completion %.
- Bar chart: Average Overall Score by Department.
- Column chart: Average Attendance % by Department.
- Slicers: Academic Year, Term, Department, Year of Study.

### Page 2 — Subject Performance
- Clustered columns: Math, Programming, and Communication scores by department.
- Matrix: Department and term with average scores.
- Scatter chart: Attendance vs Average Overall Score.

### Page 3 — Resource Allocation
- Average Library Visits by Department.
- Average Lab Hours by Department.
- Students Requiring Support by Department.
- Table of resource usage and academic indicators at aggregate level.

## Insights to investigate
- Which departments have lower average attendance or subject scores?
- How does credit completion vary by term and department?
- Are library visits or lab hours associated with higher scores?
- Where may additional academic support or lab resources be useful?

## Ethics and limitations
The dataset is synthetic and not suitable for real student decisions. Attendance and resource-use correlations do not prove causation. Do not use these measures alone to label students or allocate support. Real educational records need privacy safeguards and authorized access.

## Validation checklist
- Check StudentID uniqueness within each term; the same student may appear in multiple terms.
- Confirm attendance percentage is divided by 100 in the DAX measure.
- Format rates as percentages and scores on a 0–100 scale.
- Test filters and drill-through.
- Save the finished report as `EducationalPerformance.pbix` in this folder.