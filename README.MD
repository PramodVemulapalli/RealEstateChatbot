## Project Projo

Pramod’s implementation of a real estate chatbot in 3 days ;-)

The application is live ! You can text Projo at  **(234)-231-6345**

Here is a demo video: [https://www.youtube.com/watch?v=napNTiaft8U](https://www.youtube.com/watch?v=napNTiaft8U)
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/napNTiaft8U/0.jpg)](https://www.youtube.com/watch?v=napNTiaft8U)

## Architecture

[![IMAGE ALT TEXT HERE](https://raw.githubusercontent.com/PramodVemulapalli/RealEstateChatbot/master/docs/Architecture.png)](https://raw.githubusercontent.com/PramodVemulapalli/RealEstateChatbot/master/docs/Architecture.png)

[![IMAGE ALT TEXT HERE](https://raw.githubusercontent.com/PramodVemulapalli/RealEstateChatbot/master/docs/Dialogflowlogic.png)](https://raw.githubusercontent.com/PramodVemulapalli/RealEstateChatbot/master/docs/Dialogflowlogic.png)

The above code pertains to the flask server deployed in Heroku:

*   Connectivity to Google dialogflow is implemented in index.py
    *   The webhook() function handles two possible calls from dialogflow, one to 'fetch a house' and another to 'answer a question'.
*   Connectivity to zillow is implemented in gethomes.py which handles the two calls from dialog flow
    *   To answer the 'fetch a house' call from dialogflow there is a function getresult() which scrapes search results from zillow by encoding zipcode, max price, and bedrooms in a url and returns a single result link.  
    *   To answer the 'answer a question' call from dialogflow there is a function getreply() which takes a specific result link and a string and scrapes zillow for all the details about the house in the link such as bedrooms, bathrooms, roof, architecture type, lot size, etc and then returns a reply based on the input string.


### Getting started

*   Please use the following tutorial https://pybit.es/deploy-flask-heroku.html to deploy the flask server to heroku
*   The Heroku server needs two environment variables GOOGAUTH and GOOGLEMAPSAPIKEY to be able to access Google Dialogflow and Googlemaps api. The GOOGLEMAPSAPIKEY is a string that can be obtained as shown here https://developers.google.com/maps/documentation/javascript/get-api-key and the GOOGAUTH is a string that is the base64 encoding of the contents of the service account credentials json file that is obtained as shown here https://cloud.google.com/video-intelligence/docs/common/auth. Here is the documentation to set these variables in heroku https://devcenter.heroku.com/articles/config-vars.
*   You can import the Google Dialogflow project provided here /dialogflow/Projo.zip and import it into a newly created agent in Google Dialogflow.
*   Please use this documentation to integrate Google Dialog flow with Twilio https://cloud.google.com/dialogflow/docs/integrations/twilio


### Thanks and Credits
*   The overall app is partly based on these awesome tutorials on medium https://medium.com/zenofai/build-ai-virtual-assistant-for-travel-portal-using-dialogflow-e4ba74d4021b and https://medium.com/zenofai/build-ai-virtual-assistant-for-travel-portal-using-dialogflow-e4ba74d4021b
