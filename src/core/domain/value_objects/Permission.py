from enum import Enum


class Permission(str, Enum):
    CREATE_TODO = "create_todo"
    READ_TODO = "read_todo"
    UPDATE_TODO = "update_todo"
    DELETE_TODO = "delete_todo"