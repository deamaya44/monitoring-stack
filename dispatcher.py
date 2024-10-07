from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GOOGLE_SPACES_WEBHOOK_URL = 'Your_Google_Spaces_Webhook_here'

@app.route('/alert', methods=['POST'])
def alert():
    alert_data = request.json
    
    # Format the message according to Google Spaces requirements (JSON).
    alerts = alert_data.get('alerts', [])
    formatted_alerts = []
    
    for alert in alerts:
        formatted_alerts.append(
            f"*Alert:* {alert['annotations'].get('summary', 'No summary')}\n"
            f"*Description:* {alert['annotations'].get('description', 'No description')}\n"
            f"*Labels:*\n"
            + "\n".join([f"- {k}: {v}" for k, v in alert['labels'].items()]) + "\n"
            f"*Annotations:*\n"
            + "\n".join([f"- {k}: {v}" for k, v in alert['annotations'].items()]) + "\n"
            f"*Generator URL:* {alert['generatorURL']}\n"
            f"*Starts At:* {alert['startsAt']}\n"
            f"*Ends At:* {alert['endsAt']}\n"
        )
    
    transformed_data = {
        "text": (
            f"Alert Status: {alert_data.get('status', 'unknown')}\n"
            f"Receiver: {alert_data.get('receiver', 'unknown')}\n"
            f"External URL: {alert_data.get('externalURL', 'N/A')}\n\n"
            + "\n\n".join(formatted_alerts)
        )
    }
    
    # Send the message (alert) to Google Spaces
    response = requests.post(GOOGLE_SPACES_WEBHOOK_URL, json=transformed_data)
    
    return jsonify({"status": "alert sent", "response_code": response.status_code})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
