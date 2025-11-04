from slowapi import Limiter
from slowapi.util import get_remote_address


# Защита от спама (bruteforce).
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])
