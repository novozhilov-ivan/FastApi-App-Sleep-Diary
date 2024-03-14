from pydantic import BaseModel


class MainPageInfoSchema(BaseModel):
    main_page_info: str
