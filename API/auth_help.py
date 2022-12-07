from typing import Optional
import base64

users_db = {
    "alice": {
        "username": "alice",
        "password": "Sm9obiBEb2U="
    },
    "bob": {
        "username": "bob",
        "password": "YnVpbGRlcg=="
    },
    "clementine": {
        "username": "clementine",
        "password": "bWFuZGFyaW5l"
    },
    "admin": {
        "username": "admin",
        "password": "NGRtMU4="
    },
}

def has_rights(username : Optional[str] = None, password : Optional[str] = None) -> bool:
    if username == None or len(username) == 0:
        return False
    if password == None or len(password) == 0:
        return False
    if not username in users_db:
        return False
    
    sample_string_bytes = password.encode("ascii")
    encrypted_bytes = base64.b64encode(sample_string_bytes)
    encrypted_string = encrypted_bytes.decode("ascii")
    return users_db[username]['password'] == encrypted_string

