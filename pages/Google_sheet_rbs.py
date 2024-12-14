import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets API Setup
def connect_to_gsheet(json_keyfile, sheet_id):
    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        credentials = Credentials.from_service_account_file(json_keyfile, scopes=scopes)
        client = gspread.authorize(credentials)
        sheet = client.open_by_key(sheet_id)  # Use Google Sheet ID
        return sheet
    except FileNotFoundError:
        st.error(f"JSON file not found: {json_keyfile}. Please ensure the file exists.")
        st.stop()
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {e}")
        st.stop()

# Provide the JSON path and Google Sheet ID
GSHEET_JSON = "data/paniniwhat-6bf48ddc1d64.json"  # Replace with the correct path
GSHEET_ID = "1EUwwDXQp8rCHQ0KYf3onVLGhTGTnaDGCMzJc4hnqG_w"  # Replace with your Google Sheet ID

# Connect to Google Sheet
sheet = connect_to_gsheet(GSHEET_JSON, GSHEET_ID)
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
            st.stop()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

df = load_data()

if worksheet:
    st.success("Connected to Google Sheets successfully!")
else:
    st.error("Failed to connect to Google Sheets. Please check your credentials and permissions.")
    st.stop()

# Normalize column names to lowercase for consistent processing
df.columns = df.columns.str.strip().str.lower()

# Verify expected columns exist in the data
expected_columns = [
    "mobile_number", "date_time_stamp", "fbs", "post_bf", "pre_lunch",
    "post_lunch", "pre_dinner", "post_dinner", "2_am", "remark",
    "bolus_1", "bolus_2", "bolus_3", "basal", "advice"
]
missing_columns = [col for col in expected_columns if col not in df.columns]
if missing_columns:
    st.error(f"The following required columns are missing from the Google Sheet: {missing_columns}")
    st.stop()

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
    import hashlib
    input_hash = hashlib.sha256(input_password.encode()).hexdigest()
    return input_hash == correct_hash

# Store hashed password for doctor
CORRECT_PASSWORD_HASH = "kris"  # Pre-compute a secure hash for your password

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
