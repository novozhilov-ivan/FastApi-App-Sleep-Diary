update_note_params = {
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
                "calendar_date": {
                    "description": "desc",
                    "type": "string",
                    "format": "date",
                    "example": "2021-12-13",
                },
                "bedtime": {
                    "description": "desc",
                    "type": "string",
                    "format": "time",
                    "example": "05:30",
                },
                "asleep": {
                    "description": "desc",
                    "type": "string",
                    "format": "time",
                    "example": "12:00",
                },
                "awake": {
                    "description": "desc",
                    "type": "string",
                    "format": "time",
                    "example": "12:15",
                },
                "rise": {
                    "description": "desc",
                    "type": "string",
                    "format": "time",
                    "example": "00:19",
                },
                "time_of_night_awakenings": {
                    "description": "desc",
                    "type": "string",
                    "format": "time",
                    "example": "05:11",
                },
            },
        },
    }
}
