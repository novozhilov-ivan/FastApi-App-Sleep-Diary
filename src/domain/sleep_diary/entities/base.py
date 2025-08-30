from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(eq=False, kw_only=True, slots=True)
class BaseEntity:
    oid: UUID = field(default_factory=uuid4)
