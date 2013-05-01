import urllib, hashlib

def get_avatar_image(email):
    default = "mm" #mystery-man
    size = 40

    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'d':default, 's':str(size)})

    return gravatar_url

