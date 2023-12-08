from enums.languages_enum import LanguageEnum
from locales.translator import translate
import asyncio
from utils.message_utils import check_for_player
import os

RESPONSE_TIMEOUT = int(os.getenv('RESPONSE_TIMEOUT'))


class LanguageConfigurator:
    def __init__(self, bot):
        self.bot = bot
        self.chosen_language_code = "en-US"

    async def configure_language(self, message):
        language_options = '\n'.join([f"{lang.id} - {lang.flag}" for lang in LanguageEnum])
        # prompt_message = translate("choose_language", self.chosen_language_code) + "\n" + language_options
        prompt_message = "**Which language will the campaign be in?**\n *Please respond with a number.\n" + language_options
        await message.channel.send(prompt_message)

        try:
            response = await self.bot.wait_for('message', check=check_for_player(message.author), timeout=RESPONSE_TIMEOUT)
            selected_language = next((lang for lang in LanguageEnum if str(lang.id) == response.content.strip()), None)
            if not selected_language:
                await message.channel.send(translate("invalid_option", self.chosen_language_code))
                return None

            self.chosen_language_code = selected_language.code
            return self.chosen_language_code
        except asyncio.TimeoutError:
            await message.channel.send(translate("timeout_error", self.chosen_language_code))
            return None
