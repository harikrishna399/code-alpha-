# Power Query notes — Educational Performance

- Set score, attendance, credit, library, and lab columns to numeric types.
- Check AttendancePct and scores stay within expected ranges (0–100).
- Standardize department names and SupportFlag values.
- StudentID may repeat across terms; use StudentID + AcademicYear + Term as the natural grain for this sample.
- Avoid exposing StudentID in public reports.
- Document any missing grades and do not silently replace them with zero.