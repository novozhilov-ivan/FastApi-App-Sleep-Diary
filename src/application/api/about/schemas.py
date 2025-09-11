from pydantic import BaseModel, Field


class AboutSleepDiarySchema(BaseModel):
    description: str = Field(title="Основная информация")
