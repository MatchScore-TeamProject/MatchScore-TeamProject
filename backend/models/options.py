from enum import Enum
from datetime import date
CURR_DATE = date.today()


class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"
    DIRECTOR = "director"


# class TournamentStatus(str, Enum):
#     OPEN = "open"
#     CLOSED = "closed"


class MatchFormat(str, Enum):
    TIME = "time"
    SCORE = "score"

    # def __str__(self):
    #     return str(self.value).capitalize()


# class TournamentFormat(str, Enum):
#     KNOCKOUT = "knockout"
#     LEAGUE = "league"
#
#     # def __str__(self):
#     #     return str(self.value).capitalize()

class CurrDateTime(str, Enum):
    CURRENT_DATE = CURR_DATE


class CurrentStatus(str, Enum):
    PENDING = "pending"
    DENIED = "denied"
    APPROVED = "approved"
