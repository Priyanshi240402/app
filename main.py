from flask import Flask, request, jsonify
app = Flask(__name__)

# Verify token for GET API
verify_token = "ACETECHVENTURES"

# Dictionary to store phone_number_id, from, and msg_body
data_store = {}

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # GET API logic
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode and token:
            # Check the mode and token sent are correct
            if mode == "subscribe" and token == verify_token:
                print("WEBHOOK_VERIFIED")
                return jsonify(challenge=challenge, message="Webhook verified"), 200
            else:
                return jsonify(error="Forbidden"), 403
                return jsonify(error="Forbidden"), 403  # Respond with '403 Forbidden' if verify tokens do not match

    elif request.method == 'POST':
        # POST API logic
        body = request.get_json()

        if body and "entry" in body:
            entry = body["entry"][0]
            if "changes" in entry:
                change = entry["changes"][0]
                if "value" in change and "messages" in change["value"]:
                    message = change["value"]["messages"][0]
                    phone_number_id = change["value"]["metadata"]["phone_number_id"]
                    from_phone_number = message["from"]
                    msg_body = message["text"]["body"]

                    data_store[phone_number_id] = {"from": from_phone_number, "msg_body": msg_body}
                    return jsonify(message="Webhook received"), 200

        return jsonify(error="Invalid Request"), 400
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
                data_store[phone_number_id] = {"from": from_phone_number, "msg_body": msg_body}
                return jsonify(message="Webhook received"), 200
        else:
            return jsonify(error="No data found"), 200

    return jsonify(error="Invalid Request"), 400

if __name__ == '__main__':
    app.run(debug=True)
