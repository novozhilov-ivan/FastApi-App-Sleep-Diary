from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


@dataclass
class MixinUUIDOid:
    oid: Mapped[UUID] = mapped_column(default=uuid4, unique=True)


@dataclass
class MixinCreatedAtOnly:
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now(),
        comment="Дата создания записи",
    )


@dataclass
class MixinUpdatedAt(MixinCreatedAtOnly):
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        server_onupdate=func.now(),
        comment="Дата обновления записи",
    )
