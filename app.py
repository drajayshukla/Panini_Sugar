import streamlit as st
import pandas as pd
import datetime
import requests

# Load data from Google Sheets or local CSV (mock example)
st.title("Patient Sugar Data Management")
st.subheader("Daily Sugar Tracking System")

# WhatsApp API Details
WHATSAPP_API_URL = "https://graph.facebook.com/v16.0/<YOUR_PHONE_ID>/messages"
ACCESS_TOKEN = "<YOUR_ACCESS_TOKEN>"


def send_whatsapp_message(patient_name, fbs, pp, rbs, phone_number):
    message_data = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "template",
        "template": {
            "name": "data_confirmation",
            "language": {"code": "en_US"},
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": patient_name},
                        {"type": "text", "text": f"FBS: {fbs}, PP: {pp}, RBS: {rbs}"}
                    ]
                }
            ]
        }
    }
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.post(WHATSAPP_API_URL, json=message_data, headers=headers)
    return response


# Patient data input
patient_name = st.text_input("Enter patient name:")
phone_number = st.text_input("Enter WhatsApp number (with country code):")
fbs = st.number_input("Fasting Blood Sugar (FBS):", min_value=0)
pp = st.number_input("Postprandial Sugar (PP):", min_value=0)
rbs = st.number_input("Random Blood Sugar (RBS):", min_value=0)

if st.button("Submit and Notify"):
    # Store data (local CSV or Google Sheets)
    # Example: Save to a local CSV
    with open("patient_data.csv", "a") as f:
        f.write(f"{datetime.datetime.now()},{patient_name},{phone_number},{fbs},{pp},{rbs}\n")

    # Send WhatsApp message
    response = send_whatsapp_message(patient_name, fbs, pp, rbs, phone_number)
    if response.status_code == 200:
        st.success("Data recorded, and WhatsApp notification sent!")
    else:
        st.error(f"Failed to send WhatsApp message: {response.text}")
