import string

# Base62 alphabet (a-z, A-Z, 0-9)
ALPHABET = string.ascii_letters + string.digits

def generate_short_code(redis_conn):
    """Generates a unique short code using Redis INCR and encodes it to base62."""
    # Get a unique number by incrementing a key in Redis
    unique_id = redis_conn.incr('url_shortener:unique_id')
    short_code = encode_base62(unique_id)
    return short_code

def encode_base62(number):
    """Encodes a number to a base62 string."""
    if number == 0:
        return ALPHABET[0]
    
    base62 = []
    num = number
    while num:
        num, rem = divmod(num, 62)
        base62.append(ALPHABET[rem])
    return ''.join(reversed(base62))
