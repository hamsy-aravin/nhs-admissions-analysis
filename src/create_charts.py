import os
import matplotlib.pyplot as plt
import pandas as pd

from run_queries import run_all_queries


def ensure_output_folder():
    os.makedirs("outputs/charts", exist_ok=True)


def save_deprivation_chart(results):
    dep = results["03_deprivation_analysis"]

    plt.figure(figsize=(10, 6))
    plt.bar(
        dep["deprivation_decile"].astype(str),
        dep["emergency_pct"]
    )

    plt.title("Emergency Admission Rate by Deprivation Decile")
    plt.xlabel("Deprivation Decile (1 = Most Deprived, 10 = Least Deprived)")
    plt.ylabel("Emergency Admission Rate (%)")
    plt.tight_layout()
    plt.savefig("outputs/charts/deprivation_emergency_rate.png", dpi=300)
    plt.close()


def save_top_diagnoses_chart(results):
    top_dx = results["01_top_diagnoses"]

    overall = (
        top_dx.groupby("diagnosis_desc")["admission_count"]
        .sum()
        .nlargest(10)
        .sort_values()
        .reset_index()
    )

    plt.figure(figsize=(10, 6))
    plt.barh(overall["diagnosis_desc"], overall["admission_count"])

    plt.title("Top Diagnoses by Admission Volume")
    plt.xlabel("Admissions")
    plt.ylabel("Diagnosis")
    plt.tight_layout()
    plt.savefig("outputs/charts/top_diagnoses.png", dpi=300)
    plt.close()


def save_monthly_trends_chart(results):
    trends = results["04_admission_trends"].copy()
    trends["month"] = pd.to_datetime(trends["month"])

    plt.figure(figsize=(12, 6))

    for admission_type in trends["admission_type"].unique():
        subset = trends[trends["admission_type"] == admission_type]
        plt.plot(
            subset["month"],
            subset["admissions"],
            marker="o",
            label=admission_type
        )

    plt.title("Monthly Admissions by Type")
    plt.xlabel("Month")
    plt.ylabel("Admissions")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig("outputs/charts/monthly_trends.png", dpi=300)
    plt.close()


def save_length_of_stay_chart(results):
    los = results["02_length_of_stay"]

    top_los = (
        los.sort_values("avg_los_days", ascending=False)
        .head(10)
        .sort_values("avg_los_days")
    )

    plt.figure(figsize=(10, 6))
    plt.barh(top_los["diagnosis_desc"], top_los["avg_los_days"])

    plt.title("Diagnoses with Longest Average Length of Stay")
    plt.xlabel("Average Length of Stay (Days)")
    plt.ylabel("Diagnosis")
    plt.tight_layout()
    plt.savefig("outputs/charts/length_of_stay.png", dpi=300)
    plt.close()


def main():
    ensure_output_folder()

    print("Running SQL queries...")
    results = run_all_queries()

    print("Creating deprivation chart...")
    save_deprivation_chart(results)

    print("Creating top diagnoses chart...")
    save_top_diagnoses_chart(results)

    print("Creating monthly trends chart...")
    save_monthly_trends_chart(results)

    print("Creating length of stay chart...")
    save_length_of_stay_chart(results)

    print("Charts saved to outputs/charts/")


if __name__ == "__main__":
    main()