class NoConfigFileFound(Exception):
    def __str__(self):
        return 'No Config File found'


class OnlyPrivateChannel(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'The channel `{self.value}` is not a private channel'


class NoUserVoiceFound(Exception):
    def __str__(self):
        return f'The user have to be connected to a voice channel'
