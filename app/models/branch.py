from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from .user_branch import UserBranch
    from .user import User


class Branch(Base):
    __tablename__ = "branches"
    __table_args__ = (UniqueConstraint("name", name="uq_branches_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)

    user_branches: Mapped[list[UserBranch]] = relationship(
        "UserBranch", back_populates="branch", cascade="all, delete-orphan"
    )
    users: Mapped[list[User]] = relationship(
        "User", secondary="user_branches", back_populates="branches", lazy="selectin"
    )
