import csv
import requests

# Define your API details
url = "https://graph.facebook.com/v21.0/441279502411807/messages"  # Replace with your Phone Number ID
access_token = "EACCxpiZAJrfcBOyYyh808XACCXnz9SyvZBMuNcXKYHaf4162S30ABm8NJPor3YMrEMinDuIFDZC64Df3ace1wDx6al8naHZCsbkzP3YpPGBu6sr5udQTMcXiVqTIhLxn4eRgGUJir4N9StzUe8tRpGa4oaU3loYwgHxJrraVc8wTIsJI9H6O5jrqbAk367ViAK6hqjPDDnZCZB0ewF0XGwKcUlXmCZA6W8FBAyfZBFaNOhUZD"  # Replace with your actual access token

# Define the headers
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}


# Function to send a WhatsApp message
def send_whatsapp_message(phone_number, message_text):
    data = {
        "messaging_product": "whatsapp",
        "to": phone_number,  # Recipient's phone number
        "type": "text",  # Change to text type for custom messages
        "text": {
            "body": message_text  # Message body from CSV
        }
    }
    response = requests.post(url, json=data, headers=headers)
    return response


# Read the .csv file
csv_file = "data/recipient.csv"  # Replace with the path to your .csv file
with open(csv_file, newline='', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)

    for row in csv_reader:
        phone_number = row['phone_number']  # Column name for phone numbers

        # Construct the message dynamically
        message_text = (
            f"Dear Patient, here are your readings for today:\n"
            f"- FBS: {row['FBS']}\n"
            f"- Post-Breakfast: {row['Post-BF']}\n"
            f"- Pre-Lunch: {row['Pre-Lunch']}\n"
            f"- Post-Lunch: {row['Post-Lunch']}\n"
            f"- Pre-Dinner: {row['Pre-Dinner']}\n"
            f"- Post-Dinner: {row['Post-Dinner']}\n"
            f"- 2 AM: {row['2 AM']}\n"
            f"Thank you for sharing your data."
        )

        # Send the message
        response = send_whatsapp_message(phone_number, message_text)

        # Print the response
        if response.status_code == 200:
            print(f"Message sent successfully to {phone_number}!")
        else:
            print(f"Failed to send message to {phone_number}.")
            print(f"Status Code: {response.status_code}")
            print(response.json())
