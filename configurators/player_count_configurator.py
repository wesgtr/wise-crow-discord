from locales.translator import translate
from utils.message_utils import check_for_player
import os

RESPONSE_TIMEOUT = int(os.getenv('RESPONSE_TIMEOUT'))


class PlayerCountConfigurator:
    def __init__(self, bot):
        self.bot = bot

    async def configure_player_count(self, message, chosen_language_code, timeout):
        valid_num_players = False
        num_attempts = 0
        max_attempts = 3
        while not valid_num_players and num_attempts < max_attempts:
            await message.channel.send("**" + translate("how_many_players", chosen_language_code) + "**")
            try:
                player_response = await self.bot.wait_for('message', check=check_for_player(message.author),
                                                          timeout=RESPONSE_TIMEOUT)
                num_players = int(player_response.content)
                if num_players < 1:
                    raise ValueError
                valid_num_players = True
            except ValueError:
                await message.channel.send("Invalid number of players. Please enter a valid number.")
                num_attempts += 1

        if not valid_num_players:
            await message.channel.send("Maximum number of attempts reached. Please restart the process.")
            return

        players = [message.author] if num_players == 1 else []
        if num_players > 1:
            await message.channel.send(translate("all_players_send_message", chosen_language_code))
            for _ in range(num_players):
                player_response = await self.bot.wait_for('message', check=lambda
                    m: m.content.lower() == translate("i_am_playing",
                                                      chosen_language_code).lower() and m.author not in players and not m.author.bot,
                                                          timeout=RESPONSE_TIMEOUT)
                players.append(player_response.author)

        return {"num_players": num_players, "players": players}
