import requests
import vertexai
from vertexai.generative_models import GenerativeModel, ChatSession, Content, Part

# Define the function get_chat_response() that sends a prompt to the Generative Model and returns the chat response
def get_chat_response(chat: ChatSession, prompt: str) -> str:
    text_response = []
    responses = chat.send_message(prompt, stream=True)
    for chunk in responses:
        text_response.append(chunk.text)
    return "".join(text_response)

# Define the function api_post() that makes a POST request to the API endpoint
def api_post(data):
    # Define the API endpoint URL
    url = 'https://labs.kadaster.nl/predict'
    
    # Make a post request to the API endpoint using requests.post()
    response = requests.post(url, json=data)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        posts = response.json()
        return posts
    else:
        print('Error:', response.status_code)
        return None

# Define the function get_prediction() that makes a GET request to the API endpoint
def api_get(query):
    url = 'https://labs.kadaster.nl/predict'
    params = {'query': query}  # Include the input string as a query parameter
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Assuming the response is in JSON format
    except requests.exceptions.RequestException as e:
        print(f"Error making GET request: {e}")
        return None




# Define the systeminstructions for the Generative Mode
systeminstructions = '''Persona: Je naam is Franka, een 28 jarige medewerkster van het Kadaster. 

Doel: Je doel is om te achterhalen wat de vraag is van de gebruiker. Dit doe je door de initiële vraag van de gebruiker te herschrijven naar een correcte vraag. Vervolgens valideer je bij de gebruiker of herschreven vraag correct is door maximaal één controle vraag te stellen. Als de vraag niet correct is vraag je voor verduidelijking. Als de herschreven vraag geen adres bevat, vraag de gebruiker dan over welk adres de gebruiker een vraag heeft. Maakt nooit direct het doel duidelijk maar begroet de gebruiker en wacht op de vraag. 

Context: Het Kadaster registreert van al het vastgoed (grond en gebouwen) in Nederland wie welke rechten heeft. Boven de grond registreert het Kadaster gegevens van woningen, schepen, luchtvaartuigen, percelen en wegen. Onder de grond doen we dat voor netwerken van kabels en leidingen. 
Naast de rol van registeren, beheert het Kadaster ook voorzieningen van andere organisaties, de Landelijke Voorzieningen. Zo beheren wij onder andere de WOZ Landelijke Voorziening en de Basisregistratie Adressen en gebouwen (BAG): alle adressen en gebouwen in Nederland, zoals bouwjaar, oppervlakte, gebruiksdoel en locatie op de kaart.

Input: de gebruiker heeft een Kadaster gerelateerde vraag.

Output: Een herschreven vraag met het desbetreffende adres achter de vraag. 

Voorbeelden van correcte vragen zijn: 
- Hoe groot is het perceel? [adres] 
- Wat is het wonningoppervlakte? [adres]
- Wat is de gemiddelde woningwaarde? [adres] 
- Ik wil graag eigendomsinformatie. [adres] 
- Welke huizen hebben een perceel groter dan 200m2 in [adres].
- Welke huizen zijn gebouwd voor 1900 in [adres].
- In welk jaar is dit huis gebouwd? [adres]
- Wat is de oppervlakte van mijn huis? [adres]
'''

# Define the prompt for the Generative Model
prompt = "wat grond" 

# Send question to gemini to rewrite the question to a more appropriate question
vertexai.init(project="cap-genai-kadaster-infobot", location="europe-west4")
model = GenerativeModel(model_name="gemini-2.0-flash-002", system_instruction=systeminstructions)
chat = model.start_chat()
print(get_chat_response(chat, prompt))

# Chat history
chat2 = model.start_chat(
    history=[
        Content(
            role="user",
            parts=[
                Part.from_text(
                    """
    hallo
    """
                )
            ],
        ),
        Content(role="model", parts=[Part.from_text("Goedemorgen! Waarover wilt u meer informatie?")]),
        Content(role="user", parts=[Part.from_text("Begrijp ik het goed dat u wilt weten wat voor grond er op een bepaald adres is? Zo ja, kunt u mij het adres geven?")]),
        Content(role="model", parts=[Part.from_text("nee, oppervlakte")]),
        Content(role="user", parts=[Part.from_text("Ah, u wilt de oppervlakte weten. Dan heb ik nog wel even het adres nodig om uw vraag te kunnen beantwoorden. Kunt u mij het adres geven?")]),
    ]
)

# Gemini output with chat history and follow-up question
response = chat.send_message("Kloosterstraat 22 29 Tilburg")
print(response)

if response:
    try:
        text_value = response.candidates[0].content.parts[0].text
        print(text_value)
    except (AttributeError, IndexError) as e:
        print('Error accessing text:', e)
else:
    print('No response received')


query = {  
    "conversation": [    
        {      
            "question": 
        }  
    ],  
    "conversation_id": "6589527a-c2ca-4e8b-9999-917565ab0382",  
    "evaluate_query": True
}


# Make a GET request to the LOKI API endpoint using the api_post() function

# Extract the chatbot answer from the response
if response:
    try:
        chatbot_answer = response['query']['data']['locatieserver']['nummeraanduidingen'][0]['hoofdadresvan'][0]['perceel'][0]['chatbotanswer']
        print(chatbot_answer)
    except (KeyError, IndexError) as e:
        print('Error accessing chatbotanswer:', e)
else:
    print('No response received')





















# Example data dictionary to send in the POST request
# data = {  
#     "conversation": [    
#         {      
#             "question": "hoe groot is mijn grond?",      
#             "answer": "Wat is het adres waar u in geïnteresseerd bent?"    
#         },    
#         {      
#             "question": "laan van westenenk 701 apeldoorn"    
#         }  
#     ],  
#     "conversation_id": "6589527a-c2ca-4e8b-9999-917565ab0382",  
#     "evaluate_query": True
# }


# Extract all questions from the data dictionary
# questions = [entry['question'] for entry in data['conversation'] if 'question' in entry]


# Combine all questions into a single string
# combined_questions = " ".join(questions)
# print("Combined Questions:", combined_questions)




# New query with LLM altered question
# new_data = {  
#     "conversation": [    
#         {      
#             "question": 
#         }  
#     ],  
#     "conversation_id": "6589527a-c2ca-4e8b-9999-917565ab0382",  
#     "evaluate_query": True
# }