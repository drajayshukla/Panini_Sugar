import streamlit as st
import pandas as pd
import datetime
import requests
import os

# Application Title
st.title("Patient Sugar Data Management")
st.subheader("Daily Sugar Tracking System")

# WhatsApp API Configuration
WHATSAPP_API_URL = "https://graph.facebook.com/v16.0/441279502411807/messages"  # Replace with your Phone Number ID
ACCESS_TOKEN = "EACCxpiZAJrfcBOZC9qWgC9rNr1eruK7WJmUBOUYY3FTyzLyvlBOh8ZCg46x0akMqUHl5AfNhpmR2TpAL4moFuU1vh3iZBJPTnSAHfXAvryB9KbRYX83uSLLTFA5AxZCGpopQvl0aFZBXgFWQZBiQyZAnnZAN2CNZBfO02YdcgiF2fmi9zfZALKAARDfXc7epAkC9rcaBpL8lTdjewZDZD"

# File for storing patient data
DATA_FILE = "patient_data.csv"

# Function to send WhatsApp message
def send_whatsapp_message(patient_name, fbs, pp, rbs, phone_number):
    # Construct the message payload
    message_data = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {
            "body": f"Hello {patient_name},\nHere are your recorded sugar levels:\n"
                    f"- FBS: {fbs}\n- PP: {pp}\n- RBS: {rbs}\nThank you!"
        }
    }
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    # Send the request
    response = requests.post(WHATSAPP_API_URL, json=message_data, headers=headers)
    return response

# Load or initialize patient data
if os.path.exists(DATA_FILE):
    patient_data = pd.read_csv(DATA_FILE)
else:
    patient_data = pd.DataFrame(columns=["Timestamp", "Patient Name", "Phone Number", "FBS", "PP", "RBS"])
    patient_data.to_csv(DATA_FILE, index=False)

# Input fields for patient data
st.sidebar.header("Enter Patient Details")
patient_name = st.sidebar.text_input("Patient Name:")
phone_number = st.sidebar.text_input("WhatsApp Number (with country code):")
fbs = st.sidebar.number_input("Fasting Blood Sugar (FBS):", min_value=0)
pp = st.sidebar.number_input("Postprandial Sugar (PP):", min_value=0)
rbs = st.sidebar.number_input("Random Blood Sugar (RBS):", min_value=0)

# Submit and Notify Button
if st.sidebar.button("Submit and Notify"):
    if patient_name and phone_number:
        # Append new patient data
        new_data = pd.DataFrame({
            "Timestamp": [datetime.datetime.now()],
            "Patient Name": [patient_name],
            "Phone Number": [phone_number],
            "FBS": [fbs],
            "PP": [pp],
            "RBS": [rbs]
        })
        patient_data = pd.concat([patient_data, new_data], ignore_index=True)
        patient_data.to_csv(DATA_FILE, index=False)

        # Send WhatsApp notification
        response = send_whatsapp_message(patient_name, fbs, pp, rbs, phone_number)
        if response.status_code == 200:
            st.sidebar.success("Data recorded and WhatsApp notification sent!")
        else:
            st.sidebar.error(f"Failed to send WhatsApp message: {response.text}")
    else:
        st.sidebar.warning("Please fill all the fields before submitting!")

# Display patient data
st.write("### Recorded Patient Data")
st.dataframe(patient_data)

# Provide an option to download the patient data
st.download_button(
    label="Download Patient Data",
    data=patient_data.to_csv(index=False),
    file_name="patient_data.csv",
    mime="text/csv"
)
