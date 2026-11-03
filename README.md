# 🎓 Student Performance Dashboard

An interactive, beginner-friendly Student Performance Dashboard built using **Python, Streamlit, Pandas and Plotly**.

The dashboard helps explore student marks, attendance, grades and academic performance through interactive visualizations and key performance indicators (KPIs).

## 🚀 Features

### 1. Overview
- Key performance indicators (KPIs).
- Class average and average attendance.
- Top 5 student performance.
- Identification of students needing attention.
- Important class performance insights.

### 2. Chart Explorer
Explore 10 interactive visualizations using a single chart-selection dropdown:

1. Average Marks by Student
2. Attendance vs Performance
3. Subject-wise Average
4. Marks Distribution
5. Subject Marks Comparison (Radar Chart)
6. Student Performance Heatmap
7. Total Marks vs Attendance (Bubble Chart)
8. Grade Distribution
9. Attendance Groups vs Average Marks
10. Subject Performance Treemap

### 3. Student Analysis
- Individual student performance.
- Subject-wise marks.
- Comparison with class averages.
- Total marks, average, grade and rank.
- Attendance and at-risk status.

### 4. Data & Downloads
- View original and cleaned datasets.
- Review data quality information.
- Download processed student results as CSV.
- Download a simple HTML report.

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- Plotly
- CSV

## 📁 Project Structure

```text
student-performance-dashboard/
│
├── app.py
├── data/
│   └── student_performance.csv
│
├── pages/
│   ├── 1_Chart_Explorer.py
│   ├── 2_Student_Analysis.py
│   └── 3_Data_and_Downloads.py
│
├── utils/
│   └── helper.py
│
├── .streamlit/
│   └── config.toml
│
├── .gitignore
├── README.md
└── requirements.txt
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/student-performance-dashboard.git
```

### 2. Navigate to the project directory

```bash
cd student-performance-dashboard
```

### 3. Create a virtual environment (recommended)

```bash
python3 -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

### 5. Run the application

```bash
python3 -m streamlit run app.py
```

The dashboard will open in your browser.

## 📊 Data Cleaning and Processing

The project uses Pandas to:
- Convert numeric columns into appropriate data types.
- Handle missing values.
- Fill missing marks using the respective subject average.
- Calculate total marks and average marks.
- Assign grades based on student averages.
- Calculate student rankings.

**At-risk rule:** A student is flagged if their average mark is below 60 OR their attendance is below 75%. This is a project-defined indicator.

**Data assumption:** The current cleaning logic treats zero values as missing. In real-world datasets, zero may be a valid score and should be handled according to the data requirements.

## 🎯 Project Objective

The objective of this project is to demonstrate how Python-based data processing and visualization tools can be used to analyze student performance and present useful academic insights through an interactive dashboard.

## 👨‍💻 Author

Abhijith R

GitHub: https://github.com/AMRABHI