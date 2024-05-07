
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def query_model(messages, model="gpt-4-turbo"): 
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages
    )
    return response.choices[0].message.content



def generate_summary(messages, model="gpt-4-turbo"): 
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
    stream=True
    )

    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            yield content

