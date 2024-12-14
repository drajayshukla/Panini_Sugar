from flask import Flask, request

app = Flask(__name__)


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':  # Verification
        verify_token = "your_verify_token"
        if request.args.get('hub.verify_token') == verify_token:
            return request.args.get('hub.challenge'), 200
        return "Unauthorized", 403

    if request.method == 'POST':  # Incoming messages
        data = request.json
        print("Webhook received:", data)
        return "Event received", 200


if __name__ == "__main__":
    app.run(port=5000)
