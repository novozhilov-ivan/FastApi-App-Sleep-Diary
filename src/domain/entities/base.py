from abc import ABC
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing_extensions import Self
from uuid import UUID, uuid4


@dataclass
class BaseEntity(ABC):
    oid: UUID = field(default_factory=uuid4, kw_only=True)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
        kw_only=True,
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
        kw_only=True,
    )

    def __eq__(self: Self, other: object) -> bool:
        if not isinstance(other, BaseEntity):
            return NotImplemented
        return self.oid == other.oid

    def __hash__(self: Self) -> int:
        return hash(self.oid)