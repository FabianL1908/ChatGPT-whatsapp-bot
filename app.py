from flask import Flask, request, jsonify
import json
import logging
from chatbot import ChatBot

logging.basicConfig(filename='record.log',
                level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

bot = ChatBot()

app = Flask(__name__)

@app.route('/', methods=['POST'])
def home():
    if request.method == 'POST':
        json_data = request.json['entry'][0]['changes'][0]['value']
        if 'contacts' in json_data.keys():
            response_dict = bot.process_user_response(json_data)
            app.logger.info(response_dict)
            if response_dict["content"].lower() == "new chat":
                # Erase content of outfile_name
                open(outfile_name, 'w').close()
                return ""
            response_dict = bot.generate_chatgpt_response(json_data)
            app.logger.info(response_dict)  
        return ""


@app.route('/')
def index():
    # Used to authenticate the Meta webhook
    hub_challenge = request.args.get("hub.challenge")
    return str(hub_challenge)

if(__name__) == '__main__':
    app.run(port=5002)
