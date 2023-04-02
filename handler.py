import sys
sys.path.insert(0, 'vendor')

import openai
import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()

PREFIX = '/'
openai.api_key = os.environ.get('API_KEY')

def receive(event, context):
    message = json.loads(event['body'])

    bot_id = message['bot_id']
    response = process(message)
    if response:
        send(response, bot_id)

    return {
        'statusCode': 200,
        'body': 'ok'
    }


def process(message):
    # Prevent self-reply
    if message['sender_type'] == 'bot':
        return None
    
    if message['text'].startswith(PREFIX):
        messages = [{"role": "system", "content": "You are a helpful assistant."}, 
                    {"role": "user", "content": message['text'][len(PREFIX):].strip()}]
        response = openai.ChatCompletion.create(model="gpt-4", messages=messages)
        reply = response.choices[0].message.content
        return reply        



def send(text, bot_id):
    url = 'https://api.groupme.com/v3/bots/post'

    message = {
        'bot_id': bot_id,
        'text': text,
    }
    r = requests.post(url, json=message)