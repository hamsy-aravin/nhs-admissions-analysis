WITH diagnosis_counts AS (
    SELECT
        d.icd10_code,
        d.diagnosis_desc,
        p.region,
        COUNT(*) AS admission_count
    FROM diagnoses d
    JOIN admissions a ON d.admission_id = a.admission_id
    JOIN patients p ON a.patient_id = p.patient_id
    WHERE d.is_primary = TRUE
    GROUP BY d.icd10_code, d.diagnosis_desc, p.region
),
ranked_diagnoses AS (
    SELECT *,
        RANK() OVER (
            PARTITION BY region
            ORDER BY admission_count DESC
        ) AS rank_in_region
    FROM diagnosis_counts
)
SELECT *
FROM ranked_diagnoses
WHERE rank_in_region <= 10
ORDER BY region, rank_in_region;