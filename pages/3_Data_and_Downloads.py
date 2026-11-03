import streamlit as st
import pandas as pd
from utils.helper import load_and_clean_data, calculate_student_results

st.set_page_config(page_title="Data & Downloads", page_icon="📁", layout="wide")
st.markdown("<style>.stApp{background:#F7F6F0} h1,h2,h3{color:#164E63}</style>", unsafe_allow_html=True)
raw, cleaned = load_and_clean_data()
data = calculate_student_results(cleaned)
st.title("📁 Data & Downloads")
st.caption("Review the source data, understand cleaning and download results.")
a,b,c = st.columns(3)
a.metric("Rows in source CSV", raw.shape[0])
b.metric("Rows after cleaning", cleaned.shape[0])
c.metric("Columns", raw.shape[1])
t1,t2,t3 = st.tabs(["Cleaned data", "Original data", "Data quality"])
with t1:
    st.dataframe(data, use_container_width=True, hide_index=True)
with t2:
    st.dataframe(raw, use_container_width=True, hide_index=True)
with t3:
    quality = pd.DataFrame({"Column":raw.columns,"Missing values in source":[raw[col].isna().sum() for col in raw.columns],"Data type":[str(raw[col].dtype) for col in raw.columns]})
    st.dataframe(quality, use_container_width=True, hide_index=True)
    st.write("Source rows:", len(raw))
    st.write("Exact duplicate rows:", int(raw.duplicated().sum()))
    st.caption("The helper treats zero in marks and attendance columns as missing, then fills missing numeric values with the column mean.")
st.divider()
st.subheader("Download files")
st.download_button("⬇️ Download cleaned student results (CSV)", data.to_csv(index=False).encode("utf-8"), file_name="student_performance_results.csv", mime="text/csv")
table = data.to_html(index=False, border=0)
html = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><title>Student Performance Report</title><style>body{{font-family:Arial;background:#F7F6F0;color:#164E63;padding:28px}}table{{border-collapse:collapse;width:100%;background:white}}th{{background:#0F8B8D;color:white}}th,td{{border:1px solid #ddd;padding:9px;text-align:left}}tr:nth-child(even){{background:#f1f0e8}}</style></head><body><h1>Student Performance Report</h1><p>Generated from the Student Performance Dashboard.</p>{table}</body></html>'''
st.download_button("⬇️ Download simple HTML report", data=html.encode("utf-8"), file_name="student_performance_report.html", mime="text/html")
st.info("The HTML report is a static table report. Interactive charts remain in the Streamlit dashboard.")
