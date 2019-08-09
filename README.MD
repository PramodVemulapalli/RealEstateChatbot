

<p style="color: red; font-weight: bold">>>>>>  gd2md-html alert:  ERRORs: 0; WARNINGs: 0; ALERTS: 1.</p>
<ul style="color: red; font-weight: bold"><li>See top comment block for details on ERRORs and WARNINGs. <li>In the converted Markdown or HTML, search for inline alerts that start with >>>>>  gd2md-html alert:  for specific instances that need correction.</ul>

<p style="color: red; font-weight: bold">Links to alert messages:</p><a href="#gdcalert1">alert1</a>

<p style="color: red; font-weight: bold">>>>>> PLEASE check and correct alert issues and delete this message and the inline alerts.<hr></p>


Project Projo

Pramod’s implementation of a real estate chatbot in 3 days

The application is live ! You can text Projo at  **(234)-231-6345**

Demo Video**: **[https://www.youtube.com/watch?v=napNTiaft8U](https://www.youtube.com/watch?v=napNTiaft8U)

Architecture



<p id="gdcalert1" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/Untitled-document0.png). Store image on your image server and adjust path/filename if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert2">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/Untitled-document0.png "image_tooltip")
The above code pertains to the flask server deployed in Heroku:



*   Connectivity to Google dialogflow is implemented in index.py
    *   The webhook() function handles two possible calls from dialogflow, one to fetch a house and another to answer a question. 
*   Connectivity to zillow is implemented in gethomes.py which handles the two calls from dialog flow
    *   1) Has a function getresult() which scrapes search results from zillow by encoding zipcode, max price, and bedrooms in a url and returns a single result link.  
    *   2) Has a function getreply() which takes a specific result link and a string and scrapes zillow for all the details about the house in the link such as bedrooms, bathrooms, roof, architecture type, lot size, etc and then returns a reply based on the input string.
