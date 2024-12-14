import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import os
import hashlib

# Google Sheets API Setup
def connect_to_gsheet(json_keyfile, sheet_name):
    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        credentials = Credentials.from_service_account_file(json_keyfile, scopes=scopes)
        client = gspread.authorize(credentials)
        sheet = client.open(sheet_name)
        return sheet
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {e}")
        return None

# Load Google Sheets credentials from environment variable
GSHEET_JSON = os.getenv("GOOGLE_CREDENTIALS_PATH")  # Replace with your JSON path or set as env variable
GSHEET_NAME = "sugarchart"  # Replace with your Google Sheet name

# Connect to Google Sheet
sheet = connect_to_gsheet(GSHEET_JSON, GSHEET_NAME)
worksheet = sheet.get_worksheet(0) if sheet else None

# Load data from Google Sheet
@st.cache_data(ttl=300)  # Cache data for 5 minutes
def load_data():
    try:
        if worksheet:
            data = worksheet.get_all_records()
            return pd.DataFrame(data)
        else:
            st.error("No worksheet available. Please check your Google Sheets connection.")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

# Sidebar
st.sidebar.title("Access Portal")

# Patient View
st.sidebar.subheader("Patient Access")
mobile_number = st.sidebar.text_input("Enter your Mobile Number:")

if mobile_number:
    if mobile_number.isdigit():
        patient_data = df[df["mobile_number"].astype(str) == mobile_number]
        if not patient_data.empty:
            st.write(f"### Your Data (Mobile Number: {mobile_number})")
            st.dataframe(patient_data)
            st.download_button(
                label="Download Your Data",
                data=patient_data.to_csv(index=False),
                file_name=f"patient_{mobile_number}_data.csv",
                mime="text/csv"
            )
        else:
            st.info(f"No data found for Mobile Number: {mobile_number}.")
    else:
        st.warning("Invalid Mobile Number. Please enter a numeric value.")

# Doctor View
st.sidebar.subheader("Doctor Access")
is_doctor = st.sidebar.checkbox("I am a doctor")
doctor_password = st.sidebar.text_input("Enter Doctor Password:", type="password")

# Hash-based password authentication for security
def verify_password(input_password, correct_hash):
    input_hash = hashlib.sha256(input_password.encode()).hexdigest()
    return input_hash == correct_hash

# Store hashed password for doctor
CORRECT_PASSWORD_HASH = hashlib.sha256("securepassword123".encode()).hexdigest()  # Replace with your secure password

if is_doctor:
    if verify_password(doctor_password, CORRECT_PASSWORD_HASH):
        st.write("### All Patients' Data")
        st.dataframe(df)
        st.download_button(
            label="Download All Patient Data",
            data=df.to_csv(index=False),
            file_name="all_patient_data.csv",
            mime="text/csv"
        )
    elif doctor_password:
        st.warning("Incorrect password. Access denied.")

# Add a form to input new data
st.sidebar.title("Add New Data")
if st.sidebar.button("Add Entry"):
    st.write("### Add New Patient Data")
    mobile_number_input = st.text_input("Mobile Number")
    date_time_stamp_input = st.text_input("Date/Time Stamp")
    fbs = st.number_input("FBS", min_value=0)
    post_bf = st.number_input("Post BF", min_value=0)
    pre_lunch = st.number_input("Pre Lunch", min_value=0)
    post_lunch = st.number_input("Post Lunch", min_value=0)
    pre_dinner = st.number_input("Pre Dinner", min_value=0)
    post_dinner = st.number_input("Post Dinner", min_value=0)
    _2_am = st.number_input("2 AM", min_value=0)
    remark = st.text_area("Remark")
    bolus_1 = st.number_input("Bolus 1", min_value=0)
    bolus_2 = st.number_input("Bolus 2", min_value=0)
    bolus_3 = st.number_input("Bolus 3", min_value=0)
    basal = st.number_input("Basal", min_value=0)
    advice = st.text_area("Advice")

    if st.button("Save Entry"):
        new_row = [mobile_number_input, date_time_stamp_input, fbs, post_bf, pre_lunch, post_lunch,
                   pre_dinner, post_dinner, _2_am, remark, bolus_1, bolus_2, bolus_3, basal, advice]
        worksheet.append_row(new_row)
        st.success("New data entry added successfully!")

# Refresh Data
if st.sidebar.button("Refresh Data"):
    df = load_data()
    st.success("Data refreshed successfully!")
