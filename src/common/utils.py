from math import floor

from src.common.constants import VEC

inttup = lambda tup: tuple(map(floor, tup))
intvec = lambda vec: VEC(floor(vec.x), floor(vec.y))