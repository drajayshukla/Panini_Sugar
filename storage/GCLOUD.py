from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFY_TOKEN = "your_verify_token_here"  # Replace with your chosen token

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verification request from Facebook
        token_sent = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if token_sent == VERIFY_TOKEN:
            return challenge
        return "Invalid verification token", 403

    elif request.method == 'POST':
        # Handle incoming Webhook notifications
        data = request.get_json()
        print("Received Webhook Data:", data)
        return "Webhook received", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
