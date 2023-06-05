import Animals as aninmals

def test_eat():
    A = aninmals.Animal() # skape kortet
    A.eat(2)
    assert A.weight == 7

from biosim.animals import Animal, Annimal, Carnivore

'''
Tests-structure for island-class
- animals have attributes strength | age | f
- No other letters than W, L, H, D
- Geography must be surrounded by W (water)
- Each character must represent a cell with character code
- Each cell must have character information
- No animals in water

Not implemented yet
- water, desert, highland, lowland
- no migration yet
- Coordinate system (1,1) in upper left corner
- the first coordinate enumerates rows, the second coordinate enumerates columns

Requirements violated
- raise value error
'''
#TEST ANIMAL
# create

def test_init():
    age = 5
    weight = 20
    stat = {'age': age,
            'wieght': weight}
    animal1 = Animal(stat)

    assert animal1.age == age and animal1.weight == weight

# age / aging

# weight / loss of weight

# fittness

# migration: wait

# birth

# death

# eat

# procreate

# die

# error handling





# TEST Herbivore


# TEST Carnivore
A = Carnivore()

print(A)