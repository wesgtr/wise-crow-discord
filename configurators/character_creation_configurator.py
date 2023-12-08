from enums.environment_enum import ENVIRONMENT_MAPPING
from locales.translator import translate
from utils.message_utils import check_for_player
from enums.age_enum import AgeEnum


class CharacterCreationConfigurator:
    def __init__(self, bot):
        self.bot = bot

    async def configure_characters(self, players, selected_environment, chosen_language_code, timeout, channel):
        player_characters = {}
        for player in players:
            await channel.send(f"{player.mention}, {translate('whats_your_character_name', chosen_language_code)}")
            character_name_response = await self.bot.wait_for('message', check=check_for_player(player), timeout=timeout)
            character_name = character_name_response.content

            race_enum_class = ENVIRONMENT_MAPPING[selected_environment.name]['race']
            class_enum_class = ENVIRONMENT_MAPPING[selected_environment.name]['class']

            selected_race = await self._choose_race(player, race_enum_class, chosen_language_code, timeout, channel)
            selected_class = await self._choose_class(player, class_enum_class, chosen_language_code, timeout, channel)
            selected_age = await self._choose_age(player, chosen_language_code, timeout, channel)

            player_characters[player] = {
                "name": character_name,
                "race": selected_race,
                "class": selected_class,
                "age": selected_age
            }

        return player_characters

    async def _choose_race(self, player, race_enum, chosen_language_code, timeout, channel):
        race_options = '\n'.join([
            f"{race.value} - **{translate(race.name.lower(), chosen_language_code).upper()}**: {translate(race.name.lower() + '_description', chosen_language_code)}"
            for race in race_enum
        ])
        prompt_message = "**" + (translate("choose_race", chosen_language_code) + "**\n" + race_options)
        await channel.send(prompt_message)

        selected_race_obj = None
        while not selected_race_obj:
            race_response = await self.bot.wait_for('message', check=check_for_player(player), timeout=timeout)
            selected_race_obj = next((race for race in race_enum if str(race.value) == race_response.content.strip()), None)
            if not selected_race_obj:
                await channel.send(translate("invalid_race_option", chosen_language_code))

        return selected_race_obj.name if selected_race_obj else None

    async def _choose_class(self, player, class_enum, chosen_language_code, timeout, channel):
        class_options = '\n'.join([
            f"{class_.value} - **{translate(class_.name.lower(), chosen_language_code).upper()}**: {translate(class_.name.lower() + '_description', chosen_language_code)}"
            for class_ in class_enum
        ])
        prompt_message = "**" + (translate("choose_class", chosen_language_code) + "**\n" + class_options)
        await channel.send(prompt_message)

        selected_class_obj = None
        while not selected_class_obj:
            class_response = await self.bot.wait_for('message', check=check_for_player(player), timeout=timeout)
            selected_class_obj = next(
                (class_ for class_ in class_enum if str(class_.value) == class_response.content.strip()), None)
            if not selected_class_obj:
                await channel.send(translate("invalid_class_option", chosen_language_code))

        return selected_class_obj.name if selected_class_obj else None

    async def _choose_age(self, player, chosen_language_code, timeout, channel):
        age_options = '\n'.join(
            [f"{age.value} - {translate(age.name.lower(), chosen_language_code)}" for age in AgeEnum]
        )
        prompt_message = "**" + (translate("choose_age", chosen_language_code) + "**\n" + age_options)
        await channel.send(prompt_message)

        selected_age_obj = None
        while not selected_age_obj:
            age_response = await self.bot.wait_for('message', check=check_for_player(player), timeout=timeout)
            selected_age_obj = next((age for age in AgeEnum if str(age.value) == age_response.content.strip()), None)
            if not selected_age_obj:
                await channel.send(translate("invalid_age_option", chosen_language_code))

        return selected_age_obj.name if selected_age_obj else None

