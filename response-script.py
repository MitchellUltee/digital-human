import requests
import vertexai
from vertexai.generative_models import GenerativeModel 

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


# Example data dictionary to send in the POST request
data = {  
    "conversation": [    
        {      
            "question": "hoe groot is mijn grond?",      
            "answer": "Wat is het adres waar u in geïnteresseerd bent?"    
        },    
        {      
            "question": "laan van westenenk 701 apeldoorn"    
        }  
    ],  
    "conversation_id": "6589527a-c2ca-4e8b-9999-917565ab0382",  
    "evaluate_query": True
}

# Extract all questions from the data dictionary
questions = [entry['question'] for entry in data['conversation'] if 'question' in entry]


# Combine all questions into a single string
combined_questions = " ".join(questions)
print("Combined Questions:", combined_questions)


# Send question to gemini to rewrite the question to a more appropriate question
vertexai.init(project="cap-genai-kadaster-infobot", location="europe-west4")
model = GenerativeModel("gemini-1.5-flash-002")
model_response = model.generate_content(f"Je bent een Kadaster medewerker en wilt de vraag: '{combined_questions}' herschrijven naar Kadaster jargon. Zorg dat de vraag altijd eindigt met een vraagteken.")

print(model_response.text)


# New query with LLM altered question
new_data = {  
    "conversation": [    
        {      
            "question": model_response.text    
        }  
    ],  
    "conversation_id": "6589527a-c2ca-4e8b-9999-917565ab0382",  
    "evaluate_query": True
}

# Make a POST request to the API endpoint using the api_post() function
response = api_post(new_data)
print(response)

# Extract the chatbot answer from the response
if response:
    try:
        chatbot_answer = response['query']['data']['locatieserver']['nummeraanduidingen'][0]['hoofdadresvan'][0]['perceel'][0]['chatbotanswer']
        print(chatbot_answer)
    except (KeyError, IndexError) as e:
        print('Error accessing chatbotanswer:', e)
else:
    print('No response received')