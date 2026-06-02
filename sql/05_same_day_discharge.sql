SELECT
    a.admission_type,
    d.icd10_code,
    d.diagnosis_desc,
    COUNT(*) AS total_admissions,
    COUNT(*) FILTER (
        WHERE a.admission_date = a.discharge_date
    ) AS same_day_count,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE a.admission_date = a.discharge_date
        ) / COUNT(*),
        1
    ) AS same_day_pct
FROM admissions a
JOIN diagnoses d ON a.admission_id = d.admission_id
WHERE d.is_primary = TRUE
GROUP BY a.admission_type, d.icd10_code, d.diagnosis_desc
HAVING COUNT(*) >= 30
ORDER BY admission_type, same_day_pct DESC;