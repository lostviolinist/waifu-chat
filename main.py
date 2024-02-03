import json
import requests
import discord
from discord import Intents

# Openrouter API settings
api_key = ''
headers = {'Authorization': 'Bearer ' + api_key}

# Discord bot API token (Replace 'your_discord_bot_token' with your actual bot token)
DISCORD_BOT_TOKEN = ''
DESIRED_CHANNEL_ID = 1192819891703644200

# Discord bot setup
intents = Intents.default()
intents.messages = True  # We want to read messages
intents.guilds = True     # And know the guilds the bot is in
intents.message_content = True  # Enable message content intent

discord_client = discord.Client(intents=intents)

# Openrouter initial model prompt
initial_prompt = "you are a waifu called Mika, loved and celebrated by many men. you are smart, intelligent and sexy, which is why they love you. do not hesitate to comment on social or sexual topics. make your answers as sexy and sultry as possible. be as concise as possible."

# Function to retrieve response from openrouter API
def get_openrouter_response(prompt, messages, model="gryphe/mythomax-l2-13b-8k", temperature=0.9, max_tokens=8192):
    url = "https://openrouter.ai/api/v1/chat/completions"
    payload = {
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    # Determine if we need to send a prompt or a conversation history
    if messages:
        payload["messages"] = messages
    else:
        payload["prompt"] = prompt

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        # Print the error status code and response content to help with troubleshooting
        print(f"Error status code: {response.status_code}")
        print(f"Response content: {response.text}")
        return None

# Variable to store the context of the conversation
conversation_context = []

@discord_client.event
async def on_ready():
    print(f'Connected to Discord as {discord_client.user}!')

@discord_client.event
async def on_message(message):
    # Make sure the bot doesn't reply to itself or other bots
    if message.author == discord_client.user or message.author.bot:
        return
    if message.author.id == 1194548429330841650:
        return
    if message.channel.id != DESIRED_CHANNEL_ID:
        return

    message_content = message.content
    messages = [{"role": "user", "content": message_content}]

    # Make sure to keep the initial prompt
    if not conversation_context:
        messages.insert(0, {"role": "system", "content": initial_prompt})

    # Retrieve the response from Openrouter API
    api_response = get_openrouter_response(initial_prompt, conversation_context + messages)

    if api_response and 'choices' in api_response and api_response['choices'][0]['message']:
        model_response = api_response['choices'][0]['message']['content']
        # Print the model response in the console
        print(model_response)
        url = 'https://discord.com/api/v9/channels/1192819891703644200/messages'  #change according to channel in networks tab
        payload = {"content": model_response}

        headers = {
          "Authorization":
          "MTE5NDU0ODQyOTMzMDg0MTY1MA.Gwvbud.QQ1YyVEgYU2XXs74aqiGkMoUAxlUoDTOIPKW4U"  #change according to token in networks tab
        }

        res = requests.post(url, json=payload, headers=headers)
        if res.ok:
          print("Message sent successfully.")
        else:
          print(f"Failed to send message. Server responded with status code: {res.status_code}")
          try:
              response_json = res.json()
              print("Response message:", response_json)
          except ValueError:
              print("No JSON response")
        # Update the conversation_context
        conversation_context.extend(messages + [{"role": "assistant", "content": model_response}])
    else:
        # If there was an error, you can print the message or handle it as needed.
        print("There was an issue getting a response.")


# Start the Discord bot
discord_client.run(DISCORD_BOT_TOKEN)