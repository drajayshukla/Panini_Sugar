import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import hashlib

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
        return None
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {e}")
        return None

# Direct reference to Google Sheets JSON credentials and ID
GSHEET_JSON = "paniniwhat-6bf48ddc1d64.json"  # Replace with the correct path to your JSON file
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
            df = pd.DataFrame(data)
            if df.empty:
                st.warning("Google Sheet is empty.")
            return df
        else:
            st.error("No worksheet available. Please check your Google Sheets connection.")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

if worksheet:
    st.success("Connected to Google Sheets successfully!")
else:
    st.error("Failed to connect to Google Sheets. Please check your credentials and permissions.")
    st.stop()

# Debug loaded data
st.write("Loaded DataFrame:")
st.dataframe(df)

# Normalize column names to lowercase
df.columns = df.columns.str.strip().str.lower()

# Check for required column
if "mobile_number" not in df.columns:
    st.error("The column 'mobile_number' is missing from the Google Sheet.")
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
