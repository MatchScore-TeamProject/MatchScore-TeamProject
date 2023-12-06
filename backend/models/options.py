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


class CurrDateTime(str, Enum):
    CURRENT_DATE = CURR_DATE


class CurrentStatus(str, Enum):
    PENDING = "pending"
    DENIED = "denied"
    APPROVED = "approved"


class EmailType(str, Enum):
    LINK_REQUEST = "link_request"
    PROMOTE_REQUEST = "promote_request"
    ADDED_TO_TOURNAMENT = "tournament"
    ADDED_TO_MATCH = "match_add"
    MATCH_CHANGED = "match_changed"
