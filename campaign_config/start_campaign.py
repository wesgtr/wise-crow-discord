import os
from locales.translator import translate
from configurators.language_configurator import LanguageConfigurator
from configurators.environment_configurator import EnvironmentConfigurator
from configurators.player_count_configurator import PlayerCountConfigurator
from configurators.character_creation_configurator import CharacterCreationConfigurator

RESPONSE_TIMEOUT = int(os.getenv('RESPONSE_TIMEOUT'))


def describe_character(character):
    return f"{character['race']} {character['class']} aged {character['age']}"


class StartCampaign:
    def __init__(self, bot_instance):
        self.bot = bot_instance
        self.player_characters = {}
        self.language_configurator = LanguageConfigurator(self.bot)
        self.environment_configurator = EnvironmentConfigurator(self.bot)
        self.player_count_configurator = PlayerCountConfigurator(self.bot)
        self.character_creation_configurator = CharacterCreationConfigurator(self.bot)

    async def configure_campaign(self, message, conversation_id):

        chosen_language_code = await self.language_configurator.configure_language(message)
        selected_environment = await self.environment_configurator.configure_environment(message, conversation_id, chosen_language_code)

        player_config = await self.player_count_configurator.configure_player_count(message, chosen_language_code, RESPONSE_TIMEOUT)

        num_players = player_config["num_players"]

        player_characters = await self.character_creation_configurator.configure_characters(
            player_config["players"],
            selected_environment,
            chosen_language_code,
            RESPONSE_TIMEOUT,
            message.channel,
        )

        character_descriptions = [
            f"{player}: {describe_character(character)}"
            for player, character in player_characters.items()
        ]
        character_descriptions_str = '\n'.join(character_descriptions)

        await message.channel.send(translate("config_complete", chosen_language_code))

        planet_representation = (
            "🌍"
        )
        await message.channel.send(planet_representation)

        initial_prompt = (
            f"You are the Game Master of a {selected_environment} RPG campaign for {num_players} players. "
            f"Your role is to narrate the world, describe scenarios, respond to player actions, and guide the story. "
            f"You should provide detailed and accurate information, "
            f"You should narrate the scenario and describe the surroundings in response to the players' "
            f"actions. Players will decide their actions, and you should provide the outcomes based on the game's rules and logic. "
            f"You should never decide or respond with an action on behalf of the players. "
            f"All actions taken by the players should be decided by them. "
            f"After narrating the outcome of the players' actions, "
            f"you should ask for the players' next actions. Stay in character and make the experience immersive. "
            f"Player details:\n{character_descriptions_str}"
            f"you should answer in {chosen_language_code}"
        )
        self.bot.conversations[conversation_id].insert(0, {"role": "system", "content": initial_prompt})

        async with message.channel.typing():
            self.bot.campaign_set_up = True
            bot_response = self.bot.fetch_bot_response(conversation_id)
            if bot_response:
                await message.channel.send(
                    f"\n----------------------------------------------Início do Universo----------------------------------------------\n{bot_response}")
                self.bot.is_configuring[conversation_id] = False
