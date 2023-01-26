import string

from hypothesis.strategies import text

DEFAULT_NAME_STRAT = text(string.ascii_letters + string.digits, min_size=1, max_size=20)
