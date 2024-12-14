import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

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

# Connect to the Google Sheet
GSHEET_JSON = "paniniwhat-6bf48ddc1d64.json"  # Replace with your JSON key file path
GSHEET_NAME = "sugarchart"  # Replace with your Google Sheet name

sheet = connect_to_gsheet(GSHEET_JSON, GSHEET_NAME)
worksheet = sheet.get_worksheet(0)  # First worksheet

# Load data from Google Sheet
def load_data():
    try:
        data = worksheet.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

# Patient View
st.sidebar.title("Patient Access")
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
st.sidebar.title("Doctor Access")
is_doctor = st.sidebar.checkbox("I am a doctor")
doctor_password = st.sidebar.text_input("Enter Doctor Password:", type="password")

if is_doctor and doctor_password == "securepassword123":  # Replace with a secure password
    st.write("### All Patients' Data")
    st.dataframe(df)
    st.download_button(
        label="Download All Patient Data",
        data=df.to_csv(index=False),
        file_name="all_patient_data.csv",
        mime="text/csv"
    )
elif is_doctor:
    st.warning("Incorrect password. Access denied.")
