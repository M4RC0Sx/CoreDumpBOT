
from discord.ext.commands import CheckFailure


# General exception class.
class CustomException(Exception):
    pass


# Exception to be raised when a command is not run on a the
# channel it was designed for.
class ForbiddenChannelException(CheckFailure):
    pass
