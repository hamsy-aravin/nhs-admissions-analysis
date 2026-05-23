"""
Synthetic NHS Hospital Episode Statistics data generator.
Generates clinically plausible admission patterns for analysis.
"""

import random
import pandas as pd
import numpy as np
from datetime import date, timedelta

random.seed(42)
np.random.seed(42)

# ─────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────

REGIONS = [
    "London",
    "South East",
    "South West",
    "East of England",
    "Midlands",
    "North East and Yorkshire",
    "North West"
]

AGE_BANDS = [
    "0-9",
    "10-19",
    "20-29",
    "30-39",
    "40-49",
    "50-59",
    "60-69",
    "70+"
]

SEXES = ["Male", "Female"]

ADMISSION_TYPES = [
    "Elective",
    "Emergency",
    "Maternity",
    "Other"
]

DIAGNOSES = [
    ("I21", "Acute myocardial infarction"),
    ("I50", "Heart failure"),
    ("J18", "Pneumonia"),
    ("J44", "COPD"),
    ("K92", "Gastrointestinal haemorrhage"),
    ("N18", "Chronic kidney disease"),
    ("E11", "Type 2 diabetes mellitus"),
    ("C34", "Malignant neoplasm of bronchus"),
    ("S72", "Fracture of femur"),
    ("F32", "Depressive episode"),
    ("A41", "Sepsis"),
    ("I63", "Cerebral infarction"),
]

TREATMENTS = [
    ("K40", "Percutaneous coronary intervention"),
    ("K61", "Coronary artery bypass graft"),
    ("E85", "Fibreoptic bronchoscopy"),
    ("H01", "Total hip replacement"),
    ("H02", "Total knee replacement"),
    ("G45", "Upper GI endoscopy"),
    ("M45", "Haemodialysis"),
    ("X40", "Radiotherapy"),
    ("A01", "CT head scan"),
    ("B80", "Echocardiogram"),
]

LOS_BY_DIAGNOSIS = {
    "I21": (6, 3),
    "I50": (7, 4),
    "J18": (5, 3),
    "J44": (5, 3),
    "K92": (4, 2),
    "N18": (4, 2),
    "E11": (3, 2),
    "C34": (8, 5),
    "S72": (14, 7),
    "F32": (20, 10),
    "A41": (9, 5),
    "I63": (10, 5),
}

# ─────────────────────────────────────────────────────
# Patients
# ─────────────────────────────────────────────────────

def generate_patients(n=10000):

    patients = []

    for i in range(1, n + 1):

        deprivation = random.randint(1, 10)

        if deprivation <= 3:
            region = random.choices(
                REGIONS,
                weights=[30,10,5,10,15,20,10]
            )[0]
        else:
            region = random.choice(REGIONS)

        patients.append({
            "patient_id": i,
            "age_band": random.choices(
                AGE_BANDS,
                weights=[5,5,8,10,12,15,20,25]
            )[0],
            "sex": random.choice(SEXES),
            "region": region,
            "deprivation_decile": deprivation,
        })

    return pd.DataFrame(patients)

# ─────────────────────────────────────────────────────
# Admissions
# ─────────────────────────────────────────────────────

def generate_admissions(patients_df, n=50000):

    admissions = []

    start_date = date(2022, 1, 1)
    end_date   = date(2023, 12, 31)

    date_range = (end_date - start_date).days

    for i in range(1, n + 1):

        patient = patients_df.sample(1).iloc[0]

        deprivation = patient["deprivation_decile"]

        if deprivation <= 3:
            admission_type = random.choices(
                ADMISSION_TYPES,
                weights=[20,55,10,15]
            )[0]

        elif deprivation <= 6:
            admission_type = random.choices(
                ADMISSION_TYPES,
                weights=[35,40,12,13]
            )[0]

        else:
            admission_type = random.choices(
                ADMISSION_TYPES,
                weights=[50,25,12,13]
            )[0]

        random_days = random.randint(0, date_range)

        admission_date = start_date + timedelta(days=random_days)

        month = admission_date.month

        if admission_type == "Emergency" and month in [12,1,2]:
            if random.random() < 0.3:
                winter_day = random.randint(0, 89)

                admission_date = date(
                    random.choice([2022, 2023]),
                    12,
                    1
                ) + timedelta(days=winter_day % 31)

        icd10, _ = random.choice(DIAGNOSES)

        mean_los, std_los = LOS_BY_DIAGNOSIS[icd10]

        if admission_type == "Elective":
            los = max(
                0,
                int(np.random.normal(mean_los * 0.8,
                                     std_los * 0.7))
            )

        elif admission_type == "Emergency":
            los = max(
                0,
                int(np.random.normal(mean_los * 1.3,
                                     std_los * 1.2))
            )

        elif admission_type == "Maternity":
            los = max(1, int(np.random.normal(2,1)))

        else:
            los = max(
                0,
                int(np.random.normal(mean_los, std_los))
            )

        discharge_date = admission_date + timedelta(days=los)

        admissions.append({
            "admission_id": i,
            "patient_id": int(patient["patient_id"]),
            "admission_date": admission_date,
            "discharge_date": discharge_date,
            "admission_type": admission_type,
            "_primary_icd10": icd10,
        })

    return pd.DataFrame(admissions)

# ─────────────────────────────────────────────────────
# Diagnoses
# ─────────────────────────────────────────────────────

def generate_diagnoses(admissions_df):

    diagnoses = []

    diagnosis_id = 1

    for _, adm in admissions_df.iterrows():

        primary_icd10 = adm["_primary_icd10"]

        primary_desc = dict(DIAGNOSES)[primary_icd10]

        diagnoses.append({
            "diagnosis_id": diagnosis_id,
            "admission_id": int(adm["admission_id"]),
            "icd10_code": primary_icd10,
            "diagnosis_desc": primary_desc,
            "is_primary": True,
        })

        diagnosis_id += 1

        n_secondary = random.randint(0, 2)

        secondaries = random.sample(
            [d for d in DIAGNOSES if d[0] != primary_icd10],
            n_secondary
        )

        for icd10, desc in secondaries:

            diagnoses.append({
                "diagnosis_id": diagnosis_id,
                "admission_id": int(adm["admission_id"]),
                "icd10_code": icd10,
                "diagnosis_desc": desc,
                "is_primary": False,
            })

            diagnosis_id += 1

    return pd.DataFrame(diagnoses)

# ─────────────────────────────────────────────────────
# Treatments
# ─────────────────────────────────────────────────────

def generate_treatments(admissions_df):

    treatments = []

    treatment_id = 1

    for _, adm in admissions_df.iterrows():

        if random.random() < 0.75:

            n_treatments = random.randint(1, 3)

            selected = random.sample(TREATMENTS, n_treatments)

            for opcs, desc in selected:

                treatments.append({
                    "treatment_id": treatment_id,
                    "admission_id": int(adm["admission_id"]),
                    "opcs_code": opcs,
                    "treatment_desc": desc,
                })

                treatment_id += 1

    return pd.DataFrame(treatments)

# ─────────────────────────────────────────────────────
# Main generator
# ─────────────────────────────────────────────────────

def generate_all():

    print("Generating patients...")
    patients = generate_patients(10000)

    print("Generating admissions...")
    admissions = generate_admissions(patients, 50000)

    print("Generating diagnoses...")
    diagnoses = generate_diagnoses(admissions)

    print("Generating treatments...")
    treatments = generate_treatments(admissions)

    admissions_clean = admissions.drop(columns=["_primary_icd10"])

    print(f"Patients:   {len(patients):,}")
    print(f"Admissions: {len(admissions_clean):,}")
    print(f"Diagnoses:  {len(diagnoses):,}")
    print(f"Treatments: {len(treatments):,}")

    return patients, admissions_clean, diagnoses, treatments

# ─────────────────────────────────────────────────────
# Run script
# ─────────────────────────────────────────────────────

if __name__ == "__main__":

    patients, admissions, diagnoses, treatments = generate_all()

    print("\nSynthetic NHS data generation complete.")