# api/main.py

from flask import Flask, request, jsonify
from serverless_wsgi import handle

app = Flask(__name__)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        verify_token = "ACETECHVENTURES"
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode and token:
            # Check the mode and token sent are correct
            if mode == "subscribe" and token == verify_token:
                print("WEBHOOK_VERIFIED")
                return challenge, 200  # Respond with 200 OK and challenge token
            else:
                return "Forbidden", 403  # Respond with '403 Forbidden' if verify tokens do not match
    elif request.method == 'POST':
        # POST API logic
        body = request.get_json()

        if body.get("object"):
            if (
                body.get("entry")
                and body["entry"][0].get("changes")
                and body["entry"][0]["changes"][0]
                and body["entry"][0]["changes"][0].get("value")
                and body["entry"][0]["changes"][0]["value"].get("messages")
                and body["entry"][0]["changes"][0]["value"]["messages"][0]
            ):
                phone_number_id = body["entry"][0]["changes"][0]["value"]["metadata"]["phone_number_id"]
                from_phone_number = body["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
                msg_body = body["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]

                # Save logic will come here
                print(f"phone_number_id: {phone_number_id}, from: {from_phone_number}, msg_body: {msg_body}")
                return "Webhook received", 200
        else:
            return "No data found", 200

    return "Invalid Request", 400

def handler(event, context):
    return handle(app, event, context)
