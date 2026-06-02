WITH monthly_counts AS (
    SELECT
        DATE_TRUNC('month', admission_date) AS admission_month,
        admission_type,
        COUNT(*) AS admissions
    FROM admissions
    GROUP BY DATE_TRUNC('month', admission_date), admission_type
),
monthly_with_lag AS (
    SELECT
        admission_month,
        admission_type,
        admissions,
        LAG(admissions) OVER (
            PARTITION BY admission_type
            ORDER BY admission_month
        ) AS prev_month_admissions
    FROM monthly_counts
)
SELECT
    TO_CHAR(admission_month, 'YYYY-MM') AS month,
    admission_type,
    admissions,
    prev_month_admissions,
    CASE
        WHEN prev_month_admissions IS NULL THEN NULL
        ELSE ROUND(
            100.0 * (admissions - prev_month_admissions) / prev_month_admissions,
            1
        )
    END AS mom_change_pct
FROM monthly_with_lag
ORDER BY admission_month, admission_type;