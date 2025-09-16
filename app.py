import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Excel/CSV Log Parser", layout="wide")
st.title("📊 Excel/CSV Log Parser")

st.write("อัปโหลดไฟล์ Excel หรือ CSV ที่มีข้อมูล log อยู่ใน 1 cell แล้วระบบจะแยกข้อมูลออกมาเป็นตาราง")

uploaded_file = st.file_uploader("📂 Upload CSV or Excel file", type=["csv", "xlsx"])

# ฟังก์ชันแยกข้อมูลจากข้อความ
def parse_block(text):
    if pd.isna(text):
        return {}

    result = {}
    patterns = {
        "Use Case / Rule Name": r"Use Case / Rule Name:\s*(.*)",
        "Detected Date/Time": r"Detected Date/Time:\s*(.*)",
        "Severity Level": r"Severity Level:\s*(.*)",
        "Device / Vendor": r"Device / Vendor:\s*(.*)",
        "Event ID": r"Event ID:\s*(.*)",
        "Subject User Name": r"Subject User Name:\s*(.*)",
        "Subject Domain Name": r"Subject Domain Name:\s*(.*)",
        "Target User Name": r"Target User Name:\s*(.*)",
        "Count": r"Count:\s*(.*)",
        "Recommendation / Next Step": r"Recommendation / Next Step:\s*(.*)",
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            result[key] = match.group(1).strip()
        else:
            result[key] = ""
    return result

if uploaded_file:
    # อ่านไฟล์
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # เลือก column ที่เก็บ raw text
    col_name = st.selectbox("เลือก Column ที่เก็บข้อมูล Raw", df.columns)

    parsed_rows = df[col_name].apply(parse_block).tolist()
    parsed_df = pd.DataFrame(parsed_rows)
    final_df = pd.concat([df, parsed_df], axis=1)

    st.success("✅ แยกข้อมูลเสร็จเรียบร้อย")
    st.dataframe(final_df, use_container_width=True)

    # ดาวน์โหลดไฟล์ CSV
    csv = final_df.to_csv(index=False).encode("utf-8-sig")
    st.download_button("📥 Download CSV", data=csv, file_name="parsed_output.csv", mime="text/csv")
