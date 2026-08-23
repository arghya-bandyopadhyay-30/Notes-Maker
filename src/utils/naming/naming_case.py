def snake_to_pascal_case(value: str) -> str:
    return "".join(part.capitalize() for part in value.split("_"))
