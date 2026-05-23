# Data Dictionary — NHS Hospital Admissions

This dataset is synthetic and modelled on NHS Hospital Episode
Statistics (HES) Admitted Patient Care data. Structure and
variable definitions follow NHS Digital conventions.

---

## Table: patients

| Column             | Type    | Description                          |
|--------------------|---------|--------------------------------------|
| patient_id         | INTEGER | Unique patient identifier            |
| age_band           | TEXT    | Age group: 0-9, 10-19, ... 70+       |
| sex                | TEXT    | Male / Female / Unknown              |
| region             | TEXT    | NHS England region                   |
| deprivation_decile | INTEGER | 1 = most deprived, 10 = least        |

NHS England regions used:
London, South East, South West, East of England,
Midlands, North East and Yorkshire, North West

Deprivation decile source: Index of Multiple Deprivation (IMD)
published by the Ministry of Housing, Communities & Local Government.

---

## Table: admissions

| Column         | Type    | Description                              |
|----------------|---------|------------------------------------------|
| admission_id   | INTEGER | Unique admission identifier              |
| patient_id     | INTEGER | Foreign key → patients.patient_id        |
| admission_date | DATE    | Date patient was admitted                |
| discharge_date | DATE    | Date patient was discharged              |
| admission_type | TEXT    | Elective / Emergency / Maternity / Other |

Admission type definitions (NHS standard):

- Elective: Planned admission, non-urgent
- Emergency: Unplanned admission via A&E or urgent GP referral
- Maternity: Obstetric admission
- Other: Transfers or admissions not classified above

Length of stay = discharge_date - admission_date (days)

Same-day discharge = admission_date equals discharge_date.

---

## Table: diagnoses

| Column         | Type    | Description                              |
|----------------|---------|------------------------------------------|
| diagnosis_id   | INTEGER | Unique diagnosis identifier              |
| admission_id   | INTEGER | Foreign key → admissions.admission_id    |
| icd10_code     | TEXT    | ICD-10 diagnosis code                    |
| diagnosis_desc | TEXT    | Plain text diagnosis description         |
| is_primary     | BOOLEAN | TRUE = primary diagnosis for admission   |

ICD-10 codes used in this dataset:

| Code | Description                              |
|------|------------------------------------------|
| I21  | Acute myocardial infarction              |
| I50  | Heart failure                            |
| J18  | Pneumonia                                |
| J44  | Chronic obstructive pulmonary disease    |
| K92  | Gastrointestinal haemorrhage             |
| N18  | Chronic kidney disease                   |
| E11  | Type 2 diabetes mellitus                 |
| C34  | Malignant neoplasm of bronchus/lung      |
| S72  | Fracture of femur                        |
| F32  | Depressive episode                       |
| A41  | Sepsis                                   |
| I63  | Cerebral infarction (stroke)             |

ICD-10 is the World Health Organization international disease
classification system used throughout the NHS.

---

## Table: treatments

| Column         | Type    | Description                              |
|----------------|---------|------------------------------------------|
| treatment_id   | INTEGER | Unique treatment identifier              |
| admission_id   | INTEGER | Foreign key → admissions.admission_id    |
| opcs_code      | TEXT    | OPCS-4 procedure code                    |
| treatment_desc | TEXT    | Procedure description                    |

OPCS-4 is the NHS classification system for surgical operations
and clinical procedures.

Example procedures include:

| OPCS Code | Procedure Description                  |
|------------|----------------------------------------|
| K40        | Percutaneous coronary intervention     |
| K61        | Coronary artery bypass graft           |
| E85        | Fibreoptic bronchoscopy                |
| H01        | Total hip replacement                  |
| H02        | Total knee replacement                 |
| G45        | Upper GI endoscopy                     |
| M45        | Haemodialysis                          |
| X40        | Radiotherapy                           |
| A01        | CT head scan                           |
| B80        | Echocardiogram                         |

---

## Relationships Between Tables

- One patient can have multiple admissions
- One admission can contain multiple diagnoses
- One admission can contain multiple treatments
- Diagnoses and treatments are linked to admissions using admission_id
- Admissions are linked to patients using patient_id

---

## Data Source Note

This dataset is synthetically generated to mirror the structure
and characteristics of NHS Hospital Episode Statistics (HES)
Admitted Patient Care data.

Real HES datasets are available from NHS Digital:

https://digital.nhs.uk/data-and-information/data-tools-and-services/data-services/hospital-episode-statistics

The synthetic generation process includes clinically plausible
patterns such as:

- Higher emergency admission rates in more deprived populations
- Seasonal winter peaks in emergency admissions
- Longer lengths of stay for severe diagnoses
- Same-day discharge patterns for elective care