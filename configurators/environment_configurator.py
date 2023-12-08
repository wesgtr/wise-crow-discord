from enums.environment_enum import EnvironmentEnum
from locales.translator import translate
from utils.message_utils import check_for_player
import os

RESPONSE_TIMEOUT = int(os.getenv('RESPONSE_TIMEOUT'))


class EnvironmentConfigurator:
    def __init__(self, bot):
        self.bot = bot

    async def configure_environment(self, message, conversation_id, chosen_language_code):
        valid_environment = False
        while not valid_environment:

            environment_options = '\n'.join(
                [
                    f"{env.value} - {translate(env.name.lower() + '_name_description', chosen_language_code)}: "
                    f"{translate(env.name.lower() + '_description', chosen_language_code)}"
                    for env in
                    EnvironmentEnum]
            )
            prompt_message = "**" + (translate("choose_environment", chosen_language_code) + "**"
                                     + "\n" + translate("respond_with_number", chosen_language_code)
                                     + "\n" + environment_options)
            await message.channel.send(prompt_message)

            try:
                response = await self.bot.wait_for('message', check=check_for_player(message.author),
                                                   timeout=RESPONSE_TIMEOUT)
                self.bot.conversations[conversation_id].append({"role": "user", "content": response.content})
                selected_environment = next((env for env in EnvironmentEnum if env.value == int(response.content)),
                                            None)
                if not selected_environment:
                    raise ValueError

                valid_environment = True
                return selected_environment
            except (ValueError, IndexError):
                await message.channel.send("Invalid option. Please choose a valid option.")
