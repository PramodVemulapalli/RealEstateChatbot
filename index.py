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
    #print(data, file=sys.stdout);
    #print(json.dumps(data, indent=2, sort_keys=True), file=sys.stdout)
    myoutputcontexts=data['queryResult']['outputContexts'];
    lenofmyoutputcontexts=len(myoutputcontexts)
    #print(myoutputcontexts, file=sys.stdout)
    #print('lenoflists: ' + str(lenofmyoutputcontexts), file=sys.stdout)
    myStorage.setzipcode(myoutputcontexts[0]['parameters']['number'])
    myStorage.setupperLimit(myoutputcontexts[0]['parameters']['unit-currency']['amount'])


    #data['queryResult']['outputContexts'][0]['parameters']['number']
    #data['queryResult']['outputContexts'][0]['parameters']['unit-currency']['amount']
    #print(data['queryResult']['outputContexts']['parameters']['geo-city'], file=sys.stdout)
    if data['queryResult']['action'] == 'Findhomes.Findhomes-yes':
        reply = {}
        home_url, home_pic = myStorage.getresult()
        reply['fulfillmentText'] = str(home_url);
        reply['fulfillmentMessages'] = [{'card': {'title': 'cardtitle', 'subtitle': 'cardtext', 'imageUri': 'https://assistant.google.com/static/images/molecule/Molecule-Formation-stop.png'}}]
        reply['fulfillmentMessages'][0]['card']['imageUri']=home_pic
        #pdb.set_trace()
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
