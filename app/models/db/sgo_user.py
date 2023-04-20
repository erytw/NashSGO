from sqlalchemy.orm import mapped_column, Mapped

from app.models import dto
from app.models.db.base import Base


class SGOUser(Base):
    __tablename__ = "sgo_users"
    __mapper_args__ = {"eager_defaults": True}
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(unique=True)
    login: Mapped[str]
    password: Mapped[str]
    school: Mapped[str]

    def __repr__(self):
        return (f"<SGOUser "
                f"ID={self.tg_id} "
                f"login={self.login} "
                f"school={self.school}>"
                )

    def to_dto(self) -> dto.SGOUser:
        return dto.SGOUser(
            db_id=self.id,
            tg_id=self.tg_id,
            login=self.login,
            password=self.password,
            school=self.school,
        )
