WITH diagnosis_los AS (
    SELECT
        d.icd10_code,
        d.diagnosis_desc,
        p.region,
        COUNT(*) AS admissions,
        ROUND(AVG(a.discharge_date - a.admission_date), 1) AS avg_los,
        ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (
            ORDER BY (a.discharge_date - a.admission_date)
        )::numeric, 1) AS median_los
    FROM diagnoses d
    JOIN admissions a ON d.admission_id = a.admission_id
    JOIN patients p ON a.patient_id = p.patient_id
    WHERE d.is_primary = TRUE
    GROUP BY d.icd10_code, d.diagnosis_desc, p.region
)
SELECT
    icd10_code,
    diagnosis_desc,
    region,
    admissions,
    avg_los,
    median_los,
    RANK() OVER (ORDER BY avg_los DESC) AS los_rank_overall,
    NTILE(4) OVER (ORDER BY avg_los) AS los_quartile
FROM diagnosis_los
WHERE admissions >= 20
ORDER BY avg_los DESC;