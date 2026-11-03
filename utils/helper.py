import os
import pandas as pd

SUBJECTS = ["Python", "SQL", "Power BI", "AI"]


def load_and_clean_data():
    """Read the existing CSV, clean numeric columns and return raw and cleaned data."""
    project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(project_folder, "data", "student_performance.csv")
    raw_data = pd.read_csv(csv_path)
    data = raw_data.copy()

    for column in SUBJECTS + ["Attendance"]:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    # Existing project assumption: zero is treated as missing. Remove this loop if zero is a valid score.
    for column in SUBJECTS + ["Attendance"]:
        data.loc[data[column] == 0, column] = float("nan")

    for subject in SUBJECTS:
        data[subject] = data[subject].fillna(data[subject].mean())
    data["Attendance"] = data["Attendance"].fillna(data["Attendance"].mean())
    data = data.drop_duplicates().copy()
    for column in SUBJECTS + ["Attendance"]:
        data[column] = data[column].round(1)
    return raw_data, data


def calculate_student_results(data):
    """Add total marks, average, grade and rank."""
    data = data.copy()
    data["Total Marks"] = data[SUBJECTS].sum(axis=1).round(1)
    data["Average"] = data[SUBJECTS].mean(axis=1).round(1)

    def find_grade(average):
        if average >= 90:
            return "A+"
        elif average >= 80:
            return "A"
        elif average >= 70:
            return "B"
        elif average >= 60:
            return "C"
        else:
            return "Needs Improvement"

    data["Grade"] = data["Average"].apply(find_grade)
    data["Rank"] = data["Average"].rank(method="min", ascending=False).astype(int)
    return data
