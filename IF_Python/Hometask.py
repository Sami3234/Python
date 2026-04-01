import hmac
from hashlib import md5
key = b'DECLARATION'
h = hmac.new(key, b'', md5)
h.update(b'We hold these truths to be self-evident, that all men are created equal')
print(h.hexdigest())
