from dataclasses import dataclass
from app.core.config import settings

@dataclass(frozen=True)
class PaginationParams:
    page: int = 1
    page_size: int = settings.PAGINATIONSIZE

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size