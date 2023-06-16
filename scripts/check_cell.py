from biosim.cell import Lowland, Water, Desert
import random


cell = Lowland((1, 1))

loc = (5,5)
ls = []
for _ in range(1000):
    new = cell.get_random_neighboring_cell(loc)
    ls.append(new)
    print(new)

co = [1 for _ in ls if _ == (5,6)]
s = sum(co)
print(s)