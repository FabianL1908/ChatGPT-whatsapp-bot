import json
import requests
import openai
import os
from heyoo import WhatsApp

class ChatBot:
    def __init__(self, json_data, bot_type=None):
        self.phone_number_id = os.environ["PHONE_NUMBER_ID"]
        self.access_token = os.environ["WHATSAPP_ACCESS_TOKEN"]
        self.json_data = json_data
        self.name = json_data['contacts'][0]['profile']['name']
        self.phone_number = json_data['contacts'][0]['wa_id']
        self.message = json_data['messages'][0]['text']['body']
        if bot_type is None:
            self.bot_type = "You will be used as a Whatsapp bot. Answer as if you are a close friend."
        else:
            self.bot_type = bot_type
        self.messenger = WhatsApp(self.access_token,phone_number_id=self.phone_number_id)
    def get_outfile_name(self):
        return f'data_{self.name}_{self.phone_number}.txt'

    def process_user_response(self):
        response_dict = {"role": "user", "content": f"{self.message}"}
        outfile_name = self.get_outfile_name()
        with open(outfile_name, 'a', encoding='utf8') as outfile:
            json.dump(response_dict, outfile)
            outfile.write('\n')
        return response_dict

    def generate_chatgpt_response(self):
        messages = [{"role": "system", "content": self.bot_type}]
        outfile_name = self.get_outfile_name()
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
        self.messenger.send_message(content, self.phone_number)
        return response_dict

    def add_new_number(self, phone_number):
        self.messenger.send_template("hello_world", str(phone_number), components=[])
