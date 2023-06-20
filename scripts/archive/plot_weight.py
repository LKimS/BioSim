from matplotlib import pyplot as plt
from biosim.animals import Herbivore, Carnivore
import random
import math
import scipy.stats as stats

mu = math.log(8 ** 2 / (
    math.sqrt(8 ** 2 + 1.5 ** 2)))

sigma = math.sqrt(math.log(1 + (1.5 ** 2 / 8 ** 2)))

var1 = [random.lognormvariate(mu, sigma) for _ in range(100000)]
var2 = [random.lognormvariate(mu, sigma) for _ in range(100)]


b = stats.lognorm.fit(var1)

