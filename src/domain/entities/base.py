from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass(eq=False, kw_only=True)
class BaseEntity(ABC):
    oid: UUID = field(default_factory=uuid4)
    created_at: datetime | None = None
    updated_at: datetime | None = None
