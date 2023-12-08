def check_for_player(player):
    def _check(message):
        return message.author == player and not message.author.bot
    return _check