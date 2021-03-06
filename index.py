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
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')

    myStorage = gethomes.fromtheweb()

    # Pretty print the returned data
    print(json.dumps(data, indent=2, sort_keys=True), file=sys.stdout)
    myoutputcontexts=data['queryResult']['outputContexts'];
    contextindex = -1

    # cycle through the returned data and populate the parameters
    for x in range(len(myoutputcontexts)):
        if data['queryResult']['action'] == 'DefaultWelcomeIntent.DefaultWelcomeIntent-yes.DefaultWelcomeIntent-yes-yes' :
            if myoutputcontexts[x]['name'].rsplit('/', 1)[-1] == 'findhomes-followup' \
                or myoutputcontexts[x]['name'].rsplit('/', 1)[-1] == 'generic' :
                myStorage.setzipcode(myoutputcontexts[x]['parameters']['Zipcode'])
                myStorage.setupperLimit(myoutputcontexts[x]['parameters']['Price']['amount'])
                myStorage.setbedrooms(myoutputcontexts[x]['parameters']['Bedrooms'])
                myStorage.sethomeurl('')
                contextindex = x
        if data['queryResult']['action'] == 'DefaultWelcomeIntent.DefaultWelcomeIntent-yes.DefaultWelcomeIntent-yes-yes.DefaultWelcomeIntent-yes-yes-custom-2' :
            if myoutputcontexts[x]['name'].rsplit('/', 1)[-1] == 'defaultwelcomeintent-yes-yes-followup' :
                myStorage.setzipcode(myoutputcontexts[x]['parameters']['Zipcode'])
                myStorage.setupperLimit(myoutputcontexts[x]['parameters']['Price']['amount'])
                myStorage.setbedrooms(myoutputcontexts[x]['parameters']['Bedrooms'])
                myStorage.sethomeurl(myoutputcontexts[x]['parameters']['Homeurl'])
                replyquestion = myoutputcontexts[x]['parameters']['details']
                contextindex = x

    # check for the name of query result and act accordingly
    if data['queryResult']['action'] == 'Findhomes.Findhomes-yes' \
        or data['queryResult']['action'] == 'DefaultWelcomeIntent.DefaultWelcomeIntent-yes.DefaultWelcomeIntent-yes-yes':
        reply = {}
        home_url, home_pic = myStorage.getresult()
        print(home_url, file=sys.stdout)
        reply['fulfillmentText'] = str(home_url) + "  Say 'Show a different home' or ask questions about this home.";
        reply['fulfillmentMessages'] = [{'image': {'image_uri': 'https://assistant.google.com/static/images/molecule/Molecule-Formation-stop.png'}}]
        reply['fulfillmentMessages'][0]['image']['image_uri']=home_pic
        reply['outputContexts'] = [{"name": 'somename', "lifespanCount": 5, "parameters": { 'Homeurl' : '' }}]
        reply['outputContexts'][0]['name'] = "projects/" + str(project_id) + "/agent/sessions/unique/contexts/" + "DefaultWelcomeIntent-yes-yes-followup"
        reply['outputContexts'][0]['parameters'].update(myoutputcontexts[contextindex]['parameters'])
        reply['outputContexts'][0]['parameters']['Homeurl'] = home_url
        #reply['fulfillmentMessages'].append({'text': {'text': ['Text defined hellow']}})
        print(json.dumps(reply, indent=2, sort_keys=True), file=sys.stdout)
        #pdb.set_trace()
        return jsonify(reply)

    elif data['queryResult']['action'] == 'DefaultWelcomeIntent.DefaultWelcomeIntent-yes.DefaultWelcomeIntent-yes-yes.DefaultWelcomeIntent-yes-yes-custom-2':
        reply = {}
        reply['fulfillmentText'] = myStorage.getreply(replyquestion);
        return jsonify(reply)


    elif data['queryResult']['action'] == 'Findhomes.Findhomes-no':
        reply = {
            "fulfillmentText": "Ok. May be next time.",
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
