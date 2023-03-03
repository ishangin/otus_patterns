import secrets


def get_unique_id() -> int:
    """ this mast generate UUID4()? but for simple use rand int 4 bytes for struct.pack(i) """
    return int.from_bytes(secrets.token_bytes(4), "big", signed=True)
