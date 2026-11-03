import streamlit as st
from datetime import datetime
from utils.helper import load_and_clean_data, calculate_student_results, SUBJECTS

st.set_page_config(page_title="Student Performance Dashboard", page_icon="🎓", layout="wide")
st.markdown("""<style>
.stApp{background:#F7F6F0} [data-testid="stSidebar"]{background:#EEECE2}
h1,h2,h3{color:#164E63}
.metric-card{background:white;border:1px solid #E6E2D6;border-left:5px solid #0F8B8D;padding:16px;border-radius:12px;min-height:100px}
.metric-label{color:#64748B;font-size:.85rem}.metric-value{color:#164E63;font-size:1.8rem;font-weight:700}
.insight-card{background:white;border:1px solid #E6E2D6;border-radius:12px;padding:14px;min-height:95px}
</style>""", unsafe_allow_html=True)

raw_data, cleaned_data = load_and_clean_data()
data = calculate_student_results(cleaned_data)

st.sidebar.title("🎓 Student Dashboard")
st.sidebar.caption("Class performance at a glance")
st.sidebar.divider()
selected_student = st.sidebar.selectbox("Select student", ["All Students"] + sorted(data.Student.dropna().unique().tolist()))
minimum_average = st.sidebar.slider("Minimum average mark", 0, 100, 0)
minimum_attendance = st.sidebar.slider("Minimum attendance (%)", 0, 100, 0)
filtered = data[(data.Average >= minimum_average) & (data.Attendance >= minimum_attendance)].copy()
if selected_student != "All Students":
    filtered = filtered[filtered.Student == selected_student]

header, date = st.columns([4, 1])
with header:
    st.title("Student Performance Overview")
    st.caption("A clear view of student marks, attendance and class performance.")
with date:
    st.markdown("**📅 REPORT DATE**")
    st.markdown(f"### {datetime.now().strftime('%d %b %Y')}")
st.divider()

n = len(filtered)
class_avg = filtered.Average.mean() if n else 0
attendance_avg = filtered.Attendance.mean() if n else 0
risk = filtered[(filtered.Average < 60) | (filtered.Attendance < 75)]
pass_pct = (len(filtered[filtered.Average >= 60]) / n * 100) if n else 0
st.subheader("Class snapshot")
cols = st.columns(4)
metrics = [("Students shown", f"{n}"), ("Class average", f"{class_avg:.1f}%"), ("Average attendance", f"{attendance_avg:.1f}%"), ("At-risk students", f"{len(risk)}")]
for col, (label, value) in zip(cols, metrics):
    with col:
        st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>', unsafe_allow_html=True)
st.caption("At-risk rule: average mark below 60 OR attendance below 75%. This is a project-defined indicator, not an official academic rule.")

st.subheader("Important insights")
if n == 0:
    st.warning("No students match the selected filters. Change the filters in the sidebar.")
else:
    topper = filtered.loc[filtered.Average.idxmax()]
    subject_avg = filtered[SUBJECTS].mean()
    best_subject = subject_avg.idxmax()
    a, b, c = st.columns(3)
    cards = [("🏆 Top performer", topper.Student, f"Average: {topper.Average:.1f}%"), ("✅ Pass percentage", f"{pass_pct:.1f}%", "Average mark of 60 or above"), ("📚 Strongest subject", best_subject, f"Average: {subject_avg[best_subject]:.1f}")]
    for col, (label, value, note) in zip([a,b,c], cards):
        with col:
            st.markdown(f'<div class="insight-card"><div class="metric-label">{label}</div><b>{value}</b><br>{note}</div>', unsafe_allow_html=True)
    st.write("")
    left, right = st.columns([1.2, 1])
    with left:
        st.markdown("#### Top 5 students")
        st.dataframe(filtered.sort_values("Average", ascending=False).head(5)[["Rank","Student","Average","Attendance","Grade"]], use_container_width=True, hide_index=True)
    with right:
        st.markdown("#### Students needing attention")
        if risk.empty:
            st.success("No at-risk students in the current filter.")
        else:
            st.dataframe(risk.sort_values(["Average","Attendance"])[["Student","Average","Attendance"]], use_container_width=True, hide_index=True)
st.info("Use the pages in the left sidebar to explore all 10 charts, individual student results, data quality and downloads.")
