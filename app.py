from flask import Flask, request, jsonify
import json
import requests
import openai
import os
from heyoo import WhatsApp
import logging

logging.basicConfig(filename='record.log',
                level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
app = Flask(__name__)

@app.route('/', methods=['POST'])
def home():
    if request.method == 'POST':
        json_data = request.json['entry'][0]['changes'][0]['value']
        if 'contacts' in json_data.keys():
            name = json_data['contacts'][0]['profile']['name']
            phone_number = json_data['contacts'][0]['wa_id']
            message = json_data['messages'][0]['text']['body']
            my_dict = {"role": "user", "content": f"{message}"}
            outfile_name = f'data_{name}_{phone_number}.txt'
            print(message.lower())
            if message.lower() == "new chat":
                # Erase content of outfile_name
                open(outfile_name, 'w').close()
                return ""
            with open(outfile_name, 'a', encoding='utf8') as outfile:
                json.dump(my_dict, outfile)
                outfile.write('\n')
            app.logger.info(my_dict)
            generate_chatgpt_response(outfile_name, phone_number)
        
        return ""

def generate_chatgpt_response(outfile_name, phone_number):
#    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    messages = [{"role": "system", "content": "You will be used as an Whatsapp bot. Answer as if you are a close friend."}]
    with open(outfile_name) as f:
        for line in f.readlines():
            line_json = json.loads(line)
            messages.append(line_json)
            
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=messages)
    content = response['choices'][0]['message']['content']
    role = response['choices'][0]['message']['role']
    my_dict = {"role": role, 'content': content}
    app.logger.info(my_dict)
    with open(outfile_name, 'a', encoding='utf8') as outfile:
        json.dump(my_dict, outfile)
        outfile.write('\n')
    phone_number = phone_number
    phone_number_id = os.environ["PHONE_NUMBER_ID"]
    access_token = os.environ["WHATSAPP_ACCESS_TOKEN"]
    messenger = WhatsApp(access_token,phone_number_id=phone_number_id)
    messenger.send_message(content, phone_number)

def new_number(phone_number):
    phone_number_id = os.environ["PHONE_NUMBER_ID"]
    access_token = os.environ["WHATSAPP_ACCESS_TOKEN"]
    messenger = WhatsApp(access_token,phone_number_id=phone_number_id)
    messenger.send_template("hello_world", str(phone_number), components=[])
    

@app.route('/')
def index():
    hub_challenge = request.args.get("hub.challenge")
    return str(hub_challenge)

if(__name__) == '__main__':
    app.run(port=5002)
