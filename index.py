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

    # Pretty print the returned data
    print(json.dumps(data, indent=2, sort_keys=True), file=sys.stdout)
    myoutputcontexts=data['queryResult']['outputContexts'];

    # cycle through the returned data and populate the parameters
    for x in range(len(myoutputcontexts)):
        if myoutputcontexts[x]['name'].rsplit('/', 1)[-1] == 'findhomes-followup' \
            or myoutputcontexts[x]['name'].rsplit('/', 1)[-1] == 'defaultwelcomeintent-yes-followup' :
            myStorage.setzipcode(myoutputcontexts[x]['parameters']['Zipcode'])
            myStorage.setupperLimit(myoutputcontexts[x]['parameters']['Price']['amount'])
            myStorage.setbedrooms(myoutputcontexts[x]['parameters']['Bedrooms'])

    # check for the name of query result and act accordingly
    if data['queryResult']['action'] == 'Findhomes.Findhomes-yes' \
        or data['queryResult']['action'] == 'DefaultWelcomeIntent.DefaultWelcomeIntent-yes.DefaultWelcomeIntent-yes-yes':
        reply = {}
        home_url, home_pic = myStorage.getresult()
        reply['fulfillmentText'] = str(home_url);
        reply['fulfillmentMessages'] = [{'card': {'title': 'cardtitle', 'subtitle': 'cardtext', 'imageUri': 'https://assistant.google.com/static/images/molecule/Molecule-Formation-stop.png'}}]
        reply['fulfillmentMessages'][0]['card']['imageUri']=home_pic
        #reply['fulfillmentMessages'].append({'text': {'text': ['Text defined hellow']}})
        print(json.dumps(reply, indent=2, sort_keys=True), file=sys.stdout)
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
