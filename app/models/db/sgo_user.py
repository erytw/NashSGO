from sqlalchemy.orm import mapped_column, Mapped

from app.models.db.base import Base


class SGOUser(Base):
    __tablename__ = "sgo_users"
    __mapper_args__ = {"eager_defaults": True}
    id: Mapped[int]
    tg_id: Mapped[int] = mapped_column(unique=True, primary_key=True)
    login: Mapped[str]
    password: Mapped[str]
    school: Mapped[str]

    def __repr__(self):
        return (f"<SGOUser "
                f"ID={self.tg_id} "
                f"login={self.login} "
                f"school={self.school}>"
                )
