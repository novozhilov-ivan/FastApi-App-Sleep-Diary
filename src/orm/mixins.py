from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


@dataclass
class MetaInfo:

    oid: Mapped[UUID] = mapped_column(
        primary_key=True,
        unique=True,
        default=uuid4,
    )
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now(),
        comment="Дата создания записи",
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        server_onupdate=func.now(),
        comment="Дата обновления записи",
    )
