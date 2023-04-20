from __future__ import annotations
from dataclasses import dataclass


@dataclass
class SGOUser:
    tg_id: int
    db_id: int | None = None
    login: str | None = None
    password: str | None = None
    school: str | None = None

    @classmethod
    def from_aiogram(cls, data) -> SGOUser:
        return cls(
            tg_id=data['tg_id'],
            login=data['login'],
            password=data['password'],
            school=data['school'],
        )
