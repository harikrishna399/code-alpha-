# Educational Performance and Resource Allocation

## Objective
Evaluate academic outcomes, attendance, credits, learning support and resource capacity/use/gaps by department.

## Data files
- student_performance.csv: synthetic scores, attendance, credits and resource-use fields.
- resource_allocation.csv: 14 synthetic department/term resource observations with students, faculty, lab/library usage, tutor gaps and resource-gap score.
- DAX_Measures.dax: academic and resource measures.
- dashboard_layout.md: suggested report layout.
- dashboard.html and resource_allocation.html: supplementary browser previews.

## PBIP source
Open ../PowerBIProjects/EducationPerformance/EducationPerformance.pbip in Power BI Desktop. DepartmentTable provides a shared department dimension for student and resource tables.

## Report pages
1. Academic Performance: student count, attendance, overall score, completion, department comparison and term filter.
2. Resource Allocation & Gaps: lab utilization, gap score and resource detail by department.

## Definitions and limits
Overall score is the unweighted average of three subject averages. Lab utilization = lab hours used / capacity. Library utilization is a synthetic visit-capacity proxy, not physical occupancy. ResourceGapScore is an illustrative review indicator, not a validated index. All data are synthetic; do not use to make decisions about real students or staffing. Validate the PBIP source in Desktop and save a native PBIX when successful.
