import requests

# Define your WhatsApp API credentials and endpoint
ACCESS_TOKEN = "EACCxpiZAJrfcBOyYyh808XACCXnz9SyvZBMuNcXKYHaf4162S30ABm8NJPor3YMrEMinDuIFDZC64Df3ace1wDx6al8naHZCsbkzP3YpPGBu6sr5udQTMcXiVqTIhLxn4eRgGUJir4N9StzUe8tRpGa4oaU3loYwgHxJrraVc8wTIsJI9H6O5jrqbAk367ViAK6hqjPDDnZCZB0ewF0XGwKcUlXmCZA6W8FBAyfZBFaNOhUZD"  # Replace with your actual access token
PHONE_NUMBER_ID = "441279502411807"  # Replace with your Phone Number ID
WHATSAPP_API_URL = f"https://graph.facebook.com/v16.0/{PHONE_NUMBER_ID}/messages"

# Define the message payload
data = {
    "messaging_product": "whatsapp",
    "to": "917880499950",  # Replace with the recipient's phone number
    "type": "template",
    "template": {
        "name": "data_confirmation",  # Replace with your approved template name
        "language": {"code": "en_US"},
        "components": [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": "Dr. Shukla"},  # Replace placeholder {{1}} with "Dr. Shukla"
                    {"type": "text", "text": "FBS: 120, PP: 140, RBS: 180"}  # Replace placeholder {{2}} with sugar data
                ]
            }
        ]
    }
}

# Define the headers
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",  # Add your access token
    "Content-Type": "application/json"  # Specify the content type as JSON
}

# Send the POST request
try:
    response = requests.post(WHATSAPP_API_URL, json=data, headers=headers)

    # Handle the response
    if response.status_code == 200:
        print("Message sent successfully!")
        print(response.json())  # Print the success response
    else:
        print("Failed to send the message.")
        print(f"Status Code: {response.status_code}")
        print(response.json())  # Print the error response
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
