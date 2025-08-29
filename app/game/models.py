from sqlalchemy import BigInteger, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    first_name: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    last_name: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    username: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    best_score: Mapped[int] = mapped_column(BigInteger, default=0)
