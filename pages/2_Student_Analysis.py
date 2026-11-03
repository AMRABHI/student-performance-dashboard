import streamlit as st
import plotly.express as px
from utils.helper import load_and_clean_data, calculate_student_results, SUBJECTS

st.set_page_config(page_title="Student Analysis", page_icon="👤", layout="wide")
st.markdown("<style>.stApp{background:#F7F6F0} h1,h2,h3{color:#164E63}</style>", unsafe_allow_html=True)
_, cleaned = load_and_clean_data()
data = calculate_student_results(cleaned)
st.title("👤 Student Analysis")
st.caption("Select a student to review their individual results.")
name = st.selectbox("Select student", sorted(data.Student.tolist()))
student = data[data.Student == name].iloc[0]
a,b,c,d = st.columns(4)
a.metric("Average", f"{student['Average']:.1f}%")
b.metric("Total marks", f"{student['Total Marks']:.1f}")
c.metric("Grade", student["Grade"])
d.metric("Attendance", f"{student['Attendance']:.1f}%")
st.divider()
left,right = st.columns(2)
with left:
    st.markdown("#### Subject-wise marks")
    values = [student[s] for s in SUBJECTS]
    fig = px.bar(x=SUBJECTS, y=values, color=SUBJECTS, labels={"x":"Subject","y":"Marks"}, color_discrete_sequence=["#0F8B8D", "#FFC15E", "#9B72CF", "#EF6F6C"])
    fig.update_layout(showlegend=False, yaxis_range=[0,100])
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.markdown("#### Student marks vs class average")
    class_avg = data[SUBJECTS].mean()
    records = []
    for subject in SUBJECTS:
        records.append({"Subject":subject,"Measure":"Student","Marks":student[subject]})
        records.append({"Subject":subject,"Measure":"Class average","Marks":class_avg[subject]})
    fig2 = px.bar(records, x="Subject", y="Marks", color="Measure", barmode="group", color_discrete_map={"Student":"#0F8B8D","Class average":"#FFC15E"})
    fig2.update_layout(yaxis_range=[0,100])
    st.plotly_chart(fig2, use_container_width=True)
st.subheader("Result details")
st.dataframe(student[["Student"] + SUBJECTS + ["Total Marks","Average","Grade","Rank","Attendance"]].to_frame().T, use_container_width=True, hide_index=True)
if student["Average"] < 60 or student["Attendance"] < 75:
    st.warning("This student matches the project at-risk rule: average below 60 OR attendance below 75%.")
else:
    st.success("This student does not match the project at-risk rule.")
