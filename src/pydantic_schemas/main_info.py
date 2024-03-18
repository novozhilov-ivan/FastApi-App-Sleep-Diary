from pydantic import BaseModel


class MainPage(BaseModel):
    main_page_info: str
