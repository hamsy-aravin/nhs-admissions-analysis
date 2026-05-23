-- NHS Hospital Admissions Analysis
-- Schema: 4 tables modelled on NHS HES Admitted Patient Care data

DROP TABLE IF EXISTS treatments;
DROP TABLE IF EXISTS diagnoses;
DROP TABLE IF EXISTS admissions;
DROP TABLE IF EXISTS patients;

CREATE TABLE patients (
    patient_id         INTEGER PRIMARY KEY,
    age_band           TEXT    NOT NULL,
    sex                TEXT    NOT NULL,
    region             TEXT    NOT NULL,
    deprivation_decile INTEGER NOT NULL CHECK (deprivation_decile BETWEEN 1 AND 10)
);

CREATE TABLE admissions (
    admission_id   INTEGER PRIMARY KEY,
    patient_id     INTEGER NOT NULL,
    admission_date DATE    NOT NULL,
    discharge_date DATE    NOT NULL,
    admission_type TEXT    NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    CHECK (discharge_date >= admission_date),
    CHECK (admission_type IN ('Elective','Emergency','Maternity','Other'))
);

CREATE TABLE diagnoses (
    diagnosis_id   INTEGER PRIMARY KEY,
    admission_id   INTEGER NOT NULL,
    icd10_code     TEXT    NOT NULL,
    diagnosis_desc TEXT    NOT NULL,
    is_primary     BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (admission_id) REFERENCES admissions(admission_id)
);

CREATE TABLE treatments (
    treatment_id   INTEGER PRIMARY KEY,
    admission_id   INTEGER NOT NULL,
    opcs_code      TEXT    NOT NULL,
    treatment_desc TEXT    NOT NULL,
    FOREIGN KEY (admission_id) REFERENCES admissions(admission_id)
);

-- Indexes for query performance
CREATE INDEX idx_admissions_patient    ON admissions(patient_id);
CREATE INDEX idx_admissions_date       ON admissions(admission_date);
CREATE INDEX idx_admissions_type       ON admissions(admission_type);
CREATE INDEX idx_diagnoses_admission   ON diagnoses(admission_id);
CREATE INDEX idx_diagnoses_primary     ON diagnoses(is_primary);
CREATE INDEX idx_diagnoses_icd10       ON diagnoses(icd10_code);
CREATE INDEX idx_patients_region       ON patients(region);
CREATE INDEX idx_patients_deprivation  ON patients(deprivation_decile);