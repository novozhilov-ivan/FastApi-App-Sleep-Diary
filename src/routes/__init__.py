from src.routes.account import ns_account
from src.routes.auth import ns_auth
from src.routes.auth.refresh import ns_auth
from src.routes.auth.sign_in import ns_auth
from src.routes.auth.sign_out import ns_auth
from src.routes.auth.sign_up import ns_auth
from src.routes.diary import ns_diary
from src.routes.diary.diary import ns_diary
from src.routes.edit import ns_edit
from src.routes.edit.delete_diary import ns_edit
from src.routes.edit.export_file import ns_edit
from src.routes.edit.import_file import ns_edit
from src.routes.main import ns_main
from src.routes.notes import ns_notes

__all__ = [
    "ns_account",
    "ns_notes",
    "ns_main",
    "ns_diary",
    "ns_edit",
    "ns_auth",
]
