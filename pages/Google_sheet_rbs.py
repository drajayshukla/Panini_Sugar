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

# Load Google Sheets credentials from environment variable
GSHEET_JSON = "paniniwhat-6bf48ddc1d64.json"
if not GSHEET_JSON:
    st.error("The GOOGLE_CREDENTIALS_PATH environment variable is not set. Please configure it properly.")
    st.stop()
# Replace with your JSON path or set as env variable
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
patient_id = st.sidebar.text_input("Enter your Patient ID:")

if patient_id:
    if patient_id.isdigit():
        patient_data = df[df["Patient ID"].astype(str) == patient_id]
        if not patient_data.empty:
            st.write(f"### Your Data (Patient ID: {patient_id})")
            st.dataframe(patient_data)
            st.download_button(
                label="Download Your Data",
                data=patient_data.to_csv(index=False),
                file_name=f"patient_{patient_id}_data.csv",
                mime="text/csv"
            )
        else:
            st.info(f"No data found for Patient ID: {patient_id}.")
    else:
        st.warning("Invalid Patient ID. Please enter a numeric ID.")

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

# Refresh Data
if st.sidebar.button("Refresh Data"):
    df = load_data()
    st.success("Data refreshed successfully!")
