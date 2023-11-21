from enum import Enum


class Role:
    USER = "user"
    ADMIN = "admin"
    DIRECTOR = "director"


class TournamentStatus(Enum):
    OPEN = "open"
    CLOSED = "closed"


class MatchFormat(str, Enum):
    TIME = "time"
    SCORE = "score"

    # def __str__(self):
    #     return str(self.value).capitalize()

    # + ' limited': This concatenates the capitalized string with the literal string " limited."
    # So, when you call str(format_time) or str(format_score),
    # where format_time and format_score are instances of the MatchFormat enumeration,
    # it will return a string that looks like "Time limited" or "Score limited."


class TournamentFormat(Enum):
    KNOCKOUT = "knockout"
    LEAGUE = "league"

    def __str__(self):
        return str(self.value).capitalize()