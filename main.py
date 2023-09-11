import openai
import boto3
from pygame import mixer
from datetime import datetime

API_KEY = 'your openai api key'
AWS_ACCESS_KEY_ID = 'your aws access key'
AWS_SECRET_ACCESS_KEY = 'your aws secret key'
AWS_REGION = 'ap-south-1'
openai.api_key = API_KEY
polly_client = boto3.client('polly',
                            aws_access_key_id=AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                            region_name=AWS_REGION)
def chat_with_gpt(message):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=message,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=1.2
    )
    reply = response.choices[0].text.strip()
    return reply
def convert_text_to_speech(text):
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )
    audio_stream = response['AudioStream'].read()
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_filename = f'output_{current_time}.mp3'
    with open(output_filename, 'wb') as file:
        file.write(audio_stream)
    mixer.init()
    mixer.music.load(output_filename)
    mixer.music.play()
print("Chatbot: Hello! How can I assist you?")
while True:
    user_input = input("You: ")
    if user_input.lower() in ['bye', 'goodbye', 'see you']:
        print("Chatbot: Goodbye! Take care!")
        break
    response = chat_with_gpt(user_input)
    print("Chatbot:", response)
    convert_text_to_speech(response)
