import streamlit as st
import pandas as pd
import plotly.express as px
from utils.helper import load_and_clean_data, calculate_student_results, SUBJECTS

st.set_page_config(page_title="Chart Explorer", page_icon="📊", layout="wide")
st.markdown("<style>.stApp{background:#F7F6F0} h1,h2,h3{color:#164E63}</style>", unsafe_allow_html=True)
_, cleaned = load_and_clean_data()
data = calculate_student_results(cleaned)
st.title("📊 Chart Explorer")
st.caption("Select a chart from the dropdown. Only the selected chart will be displayed.")
options = ["Average Marks by Student", "Attendance vs Performance", "Subject-wise Average", "Marks Distribution", "Subject Marks Comparison (Radar)", "Student Performance Heatmap", "Total Marks vs Attendance (Bubble)", "Grade Distribution", "Attendance Groups vs Average Marks", "Subject Performance Treemap"]
choice = st.selectbox("Choose a chart", options)

if choice == "Average Marks by Student":
    count = st.slider("Number of students to display", 5, len(data), min(10, len(data)))
    view = data.sort_values("Average", ascending=False).head(count)
    fig = px.bar(view, x="Student", y="Average", color="Average", color_continuous_scale=["#FFC15E", "#0F8B8D", "#164E63"], title="Average marks by student")
    fig.update_layout(coloraxis_showscale=False, yaxis_title="Average mark")
    st.plotly_chart(fig, use_container_width=True)
elif choice == "Attendance vs Performance":
    fig = px.scatter(data, x="Attendance", y="Average", color="Grade", hover_name="Student", title="Attendance compared with average marks", color_discrete_sequence=["#EF6F6C", "#FFC15E", "#0F8B8D", "#9B72CF", "#164E63"])
    fig.update_layout(xaxis_title="Attendance (%)", yaxis_title="Average mark")
    st.plotly_chart(fig, use_container_width=True)
    st.metric("Attendance / average correlation", f"{data['Attendance'].corr(data['Average']):.2f}")
elif choice == "Subject-wise Average":
    view = data[SUBJECTS].mean().rename_axis("Subject").reset_index(name="Average")
    fig = px.bar(view, x="Subject", y="Average", color="Subject", title="Average marks by subject", color_discrete_sequence=["#0F8B8D", "#FFC15E", "#9B72CF", "#EF6F6C"])
    fig.update_layout(showlegend=False, yaxis_title="Average mark")
    st.plotly_chart(fig, use_container_width=True)
elif choice == "Marks Distribution":
    subject = st.selectbox("Choose subject", SUBJECTS)
    fig = px.histogram(data, x=subject, nbins=10, marginal="box", title=f"{subject} marks distribution", color_discrete_sequence=["#0F8B8D"])
    st.plotly_chart(fig, use_container_width=True)
elif choice == "Subject Marks Comparison (Radar)":
    student_name = st.selectbox("Choose student", sorted(data.Student.tolist()))
    row = data[data.Student == student_name].iloc[0]
    values = [row[s] for s in SUBJECTS]
    fig = px.line_polar(r=values, theta=SUBJECTS, line_close=True, title=f"Subject comparison for {student_name}")
    fig.update_traces(fill="toself", line_color="#0F8B8D")
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,100])))
    st.plotly_chart(fig, use_container_width=True)
elif choice == "Student Performance Heatmap":
    view = data.set_index("Student")[SUBJECTS]
    fig = px.imshow(view, text_auto=".0f", aspect="auto", color_continuous_scale=["#F7F6F0", "#FFC15E", "#0F8B8D", "#164E63"], title="Marks heatmap by student and subject")
    st.plotly_chart(fig, use_container_width=True)
elif choice == "Total Marks vs Attendance (Bubble)":
    fig = px.scatter(data, x="Attendance", y="Total Marks", size="Average", color="Grade", hover_name="Student", size_max=35, title="Total marks, attendance and average")
    fig.update_layout(xaxis_title="Attendance (%)", yaxis_title="Total marks")
    st.plotly_chart(fig, use_container_width=True)
elif choice == "Grade Distribution":
    order = ["A+", "A", "B", "C", "Needs Improvement"]
    view = data.Grade.value_counts().reindex(order, fill_value=0).rename_axis("Grade").reset_index(name="Students")
    fig = px.pie(view, names="Grade", values="Students", hole=.55, title="Student grade distribution", color_discrete_sequence=["#0F8B8D", "#9B72CF", "#FFC15E", "#EF6F6C", "#164E63"])
    st.plotly_chart(fig, use_container_width=True)
elif choice == "Attendance Groups vs Average Marks":
    view = data.copy()
    view["Attendance Group"] = pd.cut(view.Attendance, bins=[-1, 74.99, 84.99, 94.99, 100], labels=["Below 75%", "75–84%", "85–94%", "95–100%"])
    grouped = view.groupby("Attendance Group", observed=False).Average.mean().reset_index()
    fig = px.bar(grouped, x="Attendance Group", y="Average", color="Attendance Group", title="Average marks across attendance groups", color_discrete_sequence=["#EF6F6C", "#FFC15E", "#0F8B8D", "#9B72CF"])
    fig.update_layout(showlegend=False, yaxis_title="Average mark")
    st.plotly_chart(fig, use_container_width=True)
elif choice == "Subject Performance Treemap":
    view = data[SUBJECTS].mean().rename_axis("Subject").reset_index(name="Average")
    fig = px.treemap(view, path=["Subject"], values="Average", color="Average", color_continuous_scale=["#FFC15E", "#0F8B8D", "#164E63"], title="Subject performance treemap")
    st.plotly_chart(fig, use_container_width=True)
st.caption("Charts use the cleaned dataset. Missing numeric values are filled with the relevant column average by helper.py.")
