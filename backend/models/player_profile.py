from pydantic import BaseModel


class PlayerProfile(BaseModel):  # OK
    id: int | None = None
    nickname: str
    full_name: str
    country: str
    sports_club: str | None = None

    @classmethod
    def from_query_result(cls, id, nickname, full_name, country, sports_club=None):
        return cls(id=id,
                   nickname=nickname,
                   full_name=full_name,
                   country=country,
                   sports_club=sports_club)
