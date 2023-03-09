

import random
import string


characters = string.digits + string.ascii_letters
picked_chars = ''.join(random.choices(characters, k=3))
print(picked_chars)