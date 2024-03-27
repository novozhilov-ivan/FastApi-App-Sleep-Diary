from pydantic import BaseModel


class MainPageModel(BaseModel):
    main_info: str
