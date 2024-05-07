
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def query_model(messages): 
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages
    )
    return response.choices[0].message.content