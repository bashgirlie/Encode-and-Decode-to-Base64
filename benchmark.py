import base64
import re
import timeit
import binascii

# 1. Setup test payloads
# Base64 strings must be bytes or strings. We use bytes for clean processing.
short_valid = b"SGVsbG8gV29ybGQh" * 10        # ~160 chars
long_valid = b"SGVsbG8gV29ybGQh" * 1000       # ~16,000 chars
long_invalid = b"SGVsbG8gV29ybGQh" * 1000 + b"!" # Invalid character at the end

# 2. Compile regex once to keep the test fair
# This pattern strictly validates character sets and proper 4-character block layout
regex_pattern = re.compile(b"^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$")

def check_using_regex(data):
    return bool(regex_pattern.match(data))

def check_using_decode(data):
    try:
        # validate=True forces Python to reject non-base64 alphabet characters
        base64.b64decode(data, validate=True)
        return True
    except binascii.Error: # Or general Exception
        return False

# 3. Run Benchmark (10,000 cycles per test)
for name, payload in [("Short Valid", short_valid), ("Long Valid", long_valid), ("Long Invalid", long_invalid)]:
    t_regex = timeit.timeit(lambda: check_using_regex(payload), number=10000)
    t_decode = timeit.timeit(lambda: check_using_decode(payload), number=10000)
    
    print(f"--- {name} ---")
    print(f"Regex Method:  {t_regex:.5f} seconds")
    print(f"Decode Method: {t_decode:.5f} seconds")
    print(f"Speedup:       {t_regex / t_decode:.1f}x faster\n")
