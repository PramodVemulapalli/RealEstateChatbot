Project Projo

Pramod’s implementation of a real estate chatbot in 3 days

The application is live ! You can text Projo at  **(234)-231-6345**

Demo Video: [https://www.youtube.com/watch?v=napNTiaft8U](https://www.youtube.com/watch?v=napNTiaft8U)
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/napNTiaft8U/0.jpg)](https://www.youtube.com/watch?v=napNTiaft8U)

Architecture

The above code pertains to the flask server deployed in Heroku:

*   Connectivity to Google dialogflow is implemented in index.py
    *   The webhook() function handles two possible calls from dialogflow, one to fetch a house and another to answer a question.
*   Connectivity to zillow is implemented in gethomes.py which handles the two calls from dialog flow
    *   1) Has a function getresult() which scrapes search results from zillow by encoding zipcode, max price, and bedrooms in a url and returns a single result link.  
    *   2) Has a function getreply() which takes a specific result link and a string and scrapes zillow for all the details about the house in the link such as bedrooms, bathrooms, roof, architecture type, lot size, etc and then returns a reply based on the input string.
