update_note_params: dict = {
    "updated_note": {
        "in": "body",
        "name": "updated_note",
        "description": "Обновленные данные записи дневника",
        "required": True,
        "schema": {
            "type": "object",
            "minProperties": 1,
            "additionalProperties": False,
            "properties": {
                "sleep_date": {
                    "description": "desc",
                    "type": "string",
                    "format": "date",
                    "example": "2021-12-13",
                },
                "went_to_bed": {
                    "description": "desc",
                    "type": "string",
                    "format": "time",
                    "example": "05:30",
                },
                "fell_asleep": {
                    "description": "desc",
                    "type": "string",
                    "format": "time",
                    "example": "12:00",
                },
                "woke_up": {
                    "description": "desc",
                    "type": "string",
                    "format": "time",
                    "example": "12:15",
                },
                "got_up": {
                    "description": "desc",
                    "type": "string",
                    "format": "time",
                    "example": "00:19",
                },
                "no_sleep": {
                    "description": "desc",
                    "type": "string",
                    "format": "time",
                    "example": "05:11",
                },
            },
        },
    }
}
