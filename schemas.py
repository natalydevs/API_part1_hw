# schemas.py

# Общая схема данных пользователя из reqres.in
user_data_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "email": {"type": "string"},
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "avatar": {"type": "string"},
    },
    "required": ["id", "email", "first_name", "last_name", "avatar"],
    "additionalProperties": False,
}

# 1. Список пользователей: GET /api/users?page=2
list_users_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "page": {"type": "integer"},
        "per_page": {"type": "integer"},
        "total": {"type": "integer"},
        "total_pages": {"type": "integer"},
        "data": {
            "type": "array",
            "items": user_data_schema,
        },
        "support": {
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "text": {"type": "string"},
            },
            "required": ["url", "text"],
            "additionalProperties": True,
        },
    },
    "required": ["page", "per_page", "total", "total_pages", "data"],
    "additionalProperties": True,
}

# 2. Один пользователь: GET /api/users/2
single_user_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "data": user_data_schema,
        "support": {
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "text": {"type": "string"},
            },
            "required": ["url", "text"],
            "additionalProperties": True,
        },
    },
    "required": ["data"],
    "additionalProperties": True,
}

# 3. POST /api/users
post_users = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "id": {"type": "string"},
        "createdAt": {"type": "string"},
        "job": {"type": "string"},
        "name": {"type": "string"},
    },
    "required": ["id", "createdAt", "job", "name"],
}

# 4. PUT /api/users/2
put_users = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "job": {"type": "string"},
        "updatedAt": {"type": "string"},
    },
    "required": ["name", "job", "updatedAt"],
    "additionalProperties": False,
}

# 5. Ошибка регистрации: POST /api/register (400)
register_error_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "error": {"type": "string"},
    },
    "required": ["error"],
    "additionalProperties": False,
}

# Успешная регистрация: POST /api/register с email+password
register_success_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "token": {"type": "string"},
    },
    "required": ["id", "token"],
    "additionalProperties": False,
}