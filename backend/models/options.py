from enum import Enum


class Role(Enum):
    USER = "user"
    ADMIN = "admin"
    DIRECTOR = "director"

    def __str__(self):
        return str(self.value).capitalize()


class TournamentStatus(Enum):
    OPEN = "open"
    CLOSED = "closed"


# class TournamentFormat(Enum):
#     KNOCKOUT = "knockout"
#     LEAGUE = "league"


class MatchFormat(Enum):
    TIME = "time"
    SCORE = "score"

    def __str__(self):
        return str(self.value).capitalize() + ' limited'

    # + ' limited': This concatenates the capitalized string with the literal string " limited."
    # So, when you call str(format_time) or str(format_score),
    # where format_time and format_score are instances of the MatchFormat enumeration,
    # it will return a string that looks like "Time limited" or "Score limited."


class TournamentFormat(Enum):
    KNOCKOUT = "knockout"
    LEAGUE = "league"

    def __str__(self):
        return str(self.value).capitalize()
