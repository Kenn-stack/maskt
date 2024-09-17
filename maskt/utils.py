import random
import string

def gen_rand(length):
    letters =  string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

