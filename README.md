# ChatGPT-whatsapp-bot
This repository can be used to create a WhatsApp chat bot that replies with the ChatGPT API. Therefore, you have to create a Whatsapp Business account and sign up at openai. Please follow the next steps:

1. Create a WhatsApp Business Account for your app, as explained [here](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started/). This will provide you with a phone number id and a Whatsapp access token. Export them as system variables as <mark>PHONE_NUMBER_ID</mark> and WHATSAPP_ACCESS_TOKEN
2. Get an api key from openai.com. Store it as OPENAI_API_KEY.
3. Start the Flask app with `python3 app.py`.
4. Create an ngrok account to make your app public. Run: `ngrok http 5002 --region us`. It is important to choose the us location. Otherwise Meta will block your ngrok forwarding.
5. Add the ngrok url as a webhook to your WhatsApp Business App as explained [here](https://business.whatsapp.com/blog/how-to-use-webhooks-from-whatsapp-business-api).
6. Add the phone number you want to chat with to the recipients list of your WhatsApp Business App. This is step 2 in [link](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started/).
7. Run: `python3 -c "from chatbot import ChatBot; bot = ChatBot(); bot.add_new_number("49174xxxxxx")"`, where you add the phone number you want to chat with here. This will send a hello world template message to your phone number. Now you can use this chat to chat with the bot. 
8. If you want to restart the chat, just type "new chat" in the chat.
