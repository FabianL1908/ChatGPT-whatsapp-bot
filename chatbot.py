import json
import requests
import openai
import os
from heyoo import WhatsApp

class ChatBot:
    def __init__(self, bot_type=None):
        self.phone_number_id = os.environ["PHONE_NUMBER_ID"]
        self.access_token = os.environ["WHATSAPP_ACCESS_TOKEN"]
        if bot_type is None:
            self.bot_type = "You will be used as an Whatsapp bot. Answer as if you are a close friend."
        else:
            self.bot_type = bot_type
        self.messenger = WhatsApp(self.access_token,phone_number_id=self.phone_number_id)

    def get_outfile_name(self, name, phone_number):
        return f'data_{name}_{phone_number}.txt'

    def extract_user_data(self, json_data):
        name = json_data['contacts'][0]['profile']['name']
        phone_number = json_data['contacts'][0]['wa_id']
        message = json_data['messages'][0]['text']['body']
        return (name, phone_number, message)

    
    def process_user_response(self, json_data):
        name, phone_number, message = self.extract_user_data(json_data)
        response_dict = {"role": "user", "content": f"{message}"}
        outfile_name = self.get_outfile_name(name, phone_number)
        with open(outfile_name, 'a', encoding='utf8') as outfile:
            json.dump(response_dict, outfile)
            outfile.write('\n')
        return response_dict

    def generate_chatgpt_response(self, json_data):
        name, phone_number, message = self.extract_user_data(json_data)
        messages = [{"role": "system", "content": self.bot_type}]
        outfile_name = self.get_outfile_name(name, phone_number)
        with open(outfile_name) as f:
            for line in f.readlines():
                line_json = json.loads(line)
                messages.append(line_json)

        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=messages)
        content = response['choices'][0]['message']['content']
        role = response['choices'][0]['message']['role']
        response_dict = {"role": role, 'content': content}
        with open(outfile_name, 'a', encoding='utf8') as outfile:
            json.dump(response_dict, outfile)
            outfile.write('\n')
        self.messenger.send_message(content, phone_number)
        return response_dict

    def add_new_number(self, phone_number):
        self.messenger.send_template("hello_world", str(phone_number), components=[])
