from pydantic import BaseModel


class MainPage(BaseModel):
    main_info: str
