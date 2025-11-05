import secrets, time

def generate_nonce(length=24):
    return secrets.token_hex(length//2)

def ttl(seconds=180):
    return int(time.time()) + seconds
