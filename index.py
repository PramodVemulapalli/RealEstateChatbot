# /index.py
from flask import Flask, request, jsonify, render_template
import os
import dialogflow
import requests
import json
import pusher
import sys
import pdb
import gethomes

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(silent=True)
    myStorage = gethomes.fromtheweb()
    myStorage.setzipcode(data['queryResult']['outputContexts'][0]['parameters']['number'])
    myStorage.setupperLimit(data['queryResult']['outputContexts'][0]['parameters']['unit-currency']['amount'])
    #pdb.set_trace()
    print(data, file=sys.stdout)
    #data['queryResult']['outputContexts'][0]['parameters']['number']
    #data['queryResult']['outputContexts'][0]['parameters']['unit-currency']['amount']
    #print(data['queryResult']['outputContexts']['parameters']['geo-city'], file=sys.stdout)
    if data['queryResult']['action'] == 'Findhomes.Findhomes-yes':
        reply = {}
        reply['fulfillmentText'] = "Ok. Tickets booked successfully again." + str(myStorage.getresult())
        return jsonify(reply)

    elif data['queryResult']['action'] == 'Findhomes.Findhomes-no':
        reply = {
            "fulfillmentText": "Ok. Booking cancelled.",
        }
        return jsonify(reply)


@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = { "message":  fulfillment_text }
    return jsonify(response_text)


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        return response.query_result.fulfillment_text

# run Flask app
if __name__ == "__main__":
    app.run()
