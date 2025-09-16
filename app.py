import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Excel/CSV Log Parser", layout="wide")
st.title("📊 Flexible Excel/CSV Log Parser")

st.write("อัปโหลดไฟล์ Excel หรือ CSV ที่มีข้อมูล log ใน 1 cell ระบบจะดึง Key: Value ออกมาเป็นคอลัมน์อัตโนมัติ")

uploaded_file = st.file_uploader("📂 Upload CSV or Excel file", type=["csv", "xlsx"])

def parse_block(text):
    if pd.isna(text):
        return {}

    result = {}
    # จับทุกบรรทัดที่มี Key: Value
    lines = str(text).splitlines()
    for line in lines:
        match = re.match(r"^([^:]+):\s*(.*)$", line.strip())
        if match:
            key = match.group(1).strip()
            value = match.group(2).strip()
            result[key] = value
    return result

if uploaded_file:
    # อ่านไฟล์
    if uploaded_file.name.lower().endswith(".csv"):
        df = pd.read_csv(uploaded_file, dtype=str, keep_default_na=False)
    else:
        df = pd.read_excel(uploaded_file, dtype=str)

    # เลือกคอลัมน์ raw
    col_name = st.selectbox("เลือก Column ที่เก็บข้อมูล Raw", df.columns)

    parsed_rows = df[col_name].apply(parse_block).tolist()
    parsed_df = pd.DataFrame(parsed_rows)
    final_df = pd.concat([df, parsed_df], axis=1)

    st.success("✅ แยกข้อมูลเรียบร้อย (Key:Value Auto-Detect)")
    st.dataframe(final_df, use_container_width=True)

    # ดาวน์โหลด CSV
    csv = final_df.to_csv(index=False).encode("utf-8-sig")
    st.download_button("📥 Download CSV", data=csv, file_name="parsed_output.csv", mime="text/csv")
