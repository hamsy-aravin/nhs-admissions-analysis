WITH admission_summary AS (
    SELECT
        p.deprivation_decile,
        COUNT(*) AS total_admissions,
        SUM(CASE WHEN a.admission_type = 'Emergency' THEN 1 ELSE 0 END) AS emergency_admissions,
        SUM(CASE WHEN a.admission_type = 'Elective' THEN 1 ELSE 0 END) AS elective_admissions
    FROM patients p
    JOIN admissions a ON p.patient_id = a.patient_id
    GROUP BY p.deprivation_decile
)
SELECT
    deprivation_decile,
    total_admissions,
    emergency_admissions,
    elective_admissions,
    ROUND(100.0 * emergency_admissions / total_admissions, 1) AS emergency_pct,
    ROUND(100.0 * elective_admissions / total_admissions, 1) AS elective_pct
FROM admission_summary
ORDER BY deprivation_decile;