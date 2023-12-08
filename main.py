import discord
import os
from dotenv import load_dotenv
from openai_interface import get_response
from campaign_config.start_campaign import StartCampaign

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DESIRED_CHANNEL_ID = os.getenv('DESIRED_CHANNEL_ID')

intents = discord.Intents.default()
intents.message_content = True


class MyBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conversations = {}
        self.is_configuring = {}
        self.player_characters = {}
        self.campaign_set_up = False
        self.chosen_language_code = "en_US"
        self.campaign_configurator = StartCampaign(self)

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if str(message.channel.id) != DESIRED_CHANNEL_ID:
            return

        channel_id = str(message.channel.id)
        author_id = str(message.author.id)
        conversation_id = f'{channel_id}-{author_id}'

        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []

        if "start campaign" in message.content.lower() and not self.campaign_set_up:
            self.is_configuring[conversation_id] = True
            await self.campaign_configurator.configure_campaign(message, conversation_id)
            return

        if self.campaign_set_up and message.author.name in self.player_characters:
            character_name = self.player_characters[message.author.name]
            user_message = {"role": "user",
                            "content": f"{message.author.name} plays as {character_name}: {message.content}"}
            self.conversations[conversation_id].append(user_message)

            try:
                bot_response = self.fetch_bot_response(conversation_id)
                async with message.channel.typing():
                    if bot_response:
                        assistant_message = {"role": "assistant", "content": bot_response}
                        self.conversations[conversation_id].append(assistant_message)
                    else:
                        print("Bot response is empty or None.")
            except Exception as e:
                print(f"Error: {e}")

    def fetch_bot_response(self, conversation_id):
        try:
            response = get_response(self.conversations[conversation_id])
            teste = response.choices[0].message.content.strip()
            return teste
        except ValueError as e:
            print(str(e))
            return None


client = MyBot(intents=intents)
client.run(TOKEN)
