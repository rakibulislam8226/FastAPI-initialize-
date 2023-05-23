import uuid


def generate_ping_id(string_length: int = 10) -> str:
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()).upper().replace("-", "")  # Convert UUID format to a Python string.
    return random[0:string_length]  # Return the random string.
