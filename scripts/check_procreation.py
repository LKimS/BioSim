from biosim.animals import Herbivore, Carnivore
from numpy import mean, log, sqrt
from matplotlib import pyplot as plt
import random

def mu(avg, sig):
    return log(avg**2/(sqrt(avg**2 + sig**2)))

def sigma(avg, sig):
    return sqrt(log(1 + (sig**2/avg**2)))

h1_info = {'species': 'Herbivore',
                          'age': 20,
                            'weight': 100}
location = (2, 2)
h1 = Herbivore(h1_info, location)

c1_info = {'species': 'Carnivore',
                          'age': 20,
                            'weight': 50}

c1 = Carnivore(c1_info, location)

weights = []
for _ in range(10000):
    baby = c1.procreation(30)
    c1.weight = 100
    if baby is not None:
        weights.append(baby.weight)

print(mean(weights))

plt.hist(weights, bins=30)
plt.show()

random_num = [random.lognormvariate(mu(8, 1.5), sigma(8, 1.5)) for _ in range(10000)]
#plt.hist(random_num, bins=30)
#plt.show()

"""

                mu = math.log(self.w_birth**2/(math.sqrt(self.w_birth**2 + self.sigma_birth**2)))
                sigma = math.sqrt(math.log(1 + (self.sigma_birth**2/self.w_birth**2)))
                newborn_weight = random.lognormvariate(mu, sigma)"""