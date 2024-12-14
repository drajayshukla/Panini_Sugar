import requests

# Define your API details
url = "https://graph.facebook.com/v21.0/441279502411807/messages"  # Replace with your Phone Number ID
access_token = "EACCxpiZAJrfcBOZC9qWgC9rNr1eruK7WJmUBOUYY3FTyzLyvlBOh8ZCg46x0akMqUHl5AfNhpmR2TpAL4moFuU1vh3iZBJPTnSAHfXAvryB9KbRYX83uSLLTFA5AxZCGpopQvl0aFZBXgFWQZBiQyZAnnZAN2CNZBfO02YdcgiF2fmi9zfZALKAARDfXc7epAkC9rcaBpL8lTdjewZDZD"
# Define the headers
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Define the request body
data = {
    "messaging_product": "whatsapp",
    "to": "917880499950",  # Replace with the recipient's phone number
    "type": "template",
    "template": {
        "name": "hello_world",  # Replace with your template name
        "language": {
            "code": "en_US"
        }
    }
}

# Send the POST request
response = requests.post(url, json=data, headers=headers)

# Print the response
if response.status_code == 200:
    print("Message sent successfully!")
    print(response.json())
else:
    print("Failed to send the message.")
    print(f"Status Code: {response.status_code}")
    print(response.json())
