from pydantic import BaseModel


class PlayerProfile(BaseModel):  # OK
    id: int | None = None
    nickname: str | None = None
    full_name: str | None = None
    country: str | None = None
    sports_club: str | None = None

    @classmethod
    def from_query_result(cls, id, nickname, full_name, country, sports_club=None):
        return cls(id=id,
                   nickname=nickname,
                   full_name=full_name,
                   country=country,
                   sports_club=sports_club)
