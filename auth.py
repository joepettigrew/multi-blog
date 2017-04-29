import hmac
import hashlib
import random
from string import letters

secret = "lkasdjf$j89u_345n45e-jtgdf8^459u23asd"


# Global functions to create secure cookies & password hashes

# Takes the secret text to create new hash
def make_secure_val(val):
    return "%s|%s" % (val, hmac.new(secret, val).hexdigest())


# Checks the hashed value of username
def check_secure_val(secure_val):
    val = secure_val.split("|")[0]
    if secure_val == make_secure_val(val):
        return val


# Make salt for password hashing
def make_salt(length=5):
    return ''.join(random.choice(letters) for x in xrange(length))


# Make the password hash with salt
def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)


# Validate the password
def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)
