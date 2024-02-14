from flask import Flask, request, jsonify

app = Flask(__name__)

verify_token = "ACETECHVENTURES"
data_store = {}

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode and token:
            if mode == "subscribe" and token == verify_token:
                print("WEBHOOK_VERIFIED")
                return jsonify(challenge=challenge), 200
            else:
                return jsonify(error="Forbidden"), 403

    elif request.method == 'POST':
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

if __name__ == '__main__':
    app.run(debug=True)

