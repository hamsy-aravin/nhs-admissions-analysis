SELECT
    a.admission_type,
    d.icd10_code,
    d.diagnosis_desc,
    COUNT(*) AS total_admissions,
    ROUND(AVG(a.discharge_date - a.admission_date), 1) AS avg_los_days,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (
        ORDER BY (a.discharge_date - a.admission_date)
    )::numeric, 1) AS median_los_days
FROM admissions a
JOIN diagnoses d ON a.admission_id = d.admission_id
WHERE d.is_primary = TRUE
GROUP BY a.admission_type, d.icd10_code, d.diagnosis_desc
HAVING COUNT(*) >= 50
ORDER BY avg_los_days DESC;