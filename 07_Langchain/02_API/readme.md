## Getting Started

To get started, make sure you have Python 3.7 or higher installed. Then, install the required packages by running:


###### pip install -r requirements.txt
Next, create a .env file in the root directory of the project and add the following environment variable:


*OLLAMA_MODEL=phi3
Finally, run the app by executing:


*uvicorn app:app --host localhost --port 8000
##### Endpoints
The app provides two endpoints for generating text:

*/essay
*Generates an essay about a given topic with 100 words.

*Request:

*json

*{
 "topic": "artificial intelligence"
*}
###### Response:

*json

*{
  "text": "Artificial intelligence (AI) is a branch of computer science that aims to create machines that mimic human intelligence. AI has the potential to revolutionize many industries, from healthcare to transportation. However, it also raises ethical concerns, such as job displacement and privacy issues. Despite these challenges, AI is here to stay and will continue to shape our world in the years to come."
*}

*/poem
##### Generates a poem about a given topic with 100 words.

*Request*:

json

{
  "topic": "love"
}
Response:

**json**

{
  "text": "Love, a force so strong and true,\nA feeling that can lift us high or bring us low.\nIt can heal our wounds and soothe our souls,\nOr it can break our hearts and leave us cold.\nBut no matter the pain, we cannot resist,\nThe allure of love, its gentle kiss.\nFor in the end, it is love that we seek,\nA connection that is deep and unique."
}