# BioSim: Modelling the ecosystem of Rossumøya

## Background
The Environmental Protection Agency of Pylandia (EPAP)
established research groups to develop a simulation of
the population dynamics of Rossumøya. The long term goal
is to use the simulation to preserve Rossumøya as a nature
park for further generations.

## Project mandate
Create a simulation of Rossumøya with animals living
and migration on the island through generations.

## Prerequisites
To use this software you need to have `Python 3.11` and with `scipy`, `numpy` and `matplotlib`.
If you want to run the included tests, then you also need the python package: `pytest`.

## Installation

## Usage

An example code of how to use this package is shown below.


```python
from biosim.simulation import BioSim
geogr = """\
               WWWWWWWWWWWWWWWWWWWWW
               WWWWWWWWHWWWWLLLLLLLW
               WHHHHHLLLLWWLLLLLLLWW
               WHHHHHHHHHWWLLLLLLWWW
               WHHHHHLLLLLLLLLLLLWWW
               WHHHHHLLLDDLLLHLLLWWW
               WHHLLLLLDDDLLLHHHHWWW
               WWHHHHLLLDDLLLHWWWWWW
               WHHHLLLLLDDLLLLLLLWWW
               WHHHHLLLLDDLLLLWWWWWW
               WWHHHHLLLLLLLLWWWWWWW
               WWWHHHHLLLLLLLWWWWWWW
               WWWWWWWWWWWWWWWWWWWWW"""


ini_herbs = [{'loc': (3, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(150)]}]
ini_carns = [{'loc': (3, 2),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(40)]}]
sim = BioSim(island_map=geogr, ini_pop=ini_herbs, img_dir='images')

sim.simulate(num_years=100)
sim.add_population(population=ini_carns)
sim.simulate(num_years=100)

sim.make_movie()
```


First you import the BioSim class from the simulation module. 
Then you create a string that represents the map of the island. 
The map is a grid of cells, where each cell is either water (W), desert (D), 
lowland (L) or highland (H) and has to be surrounded by water. All the lines in this string has to be the same length.


The upper left corner of the map has coordinates (0, 0). 
Coordiantes (1,0) is the cell below (0, 0) and (0, 1) is the cell to the right of (0, 0).

To create an instance of BioSim, you need to give the map string as a parameter. 
You can either add animals to the simulation by giving the ini_pop parameter to the BioSim class,
or you can add animals to the simulation later by using the add_population method.
These two methods of adding animals take in a list of dictionaries as a parameter, as shown above.

The simulation is run by calling the simulate method, which will create a live visualization of the simulation.
The simulation can be run for a given number of years by giving the num_years parameter to the simulate method.
After which you can eiter add more animals to the simulation and continue the simulation or stop. 
If you choose to give an img_dir parameter to the BioSim class, 
then the simulation will save images of the simulation to the given directory. If you call the make_movie method, 
then the images will be combined into a video. Here is a live visualization of the simulation:

<!-- <img src="docs/figures/live.png" alt="Logo" width="1120" height="630"> -->

![sample](https://github.com/LKimS/BioSim/assets/146383468/bbbd6d70-5a0c-4dc5-bd50-a799bcc19a36)


### Valid params
The following parameters can be given to the BioSim class:
- island_map: A string representing the map of the island. 
Must be a rectangle of cells, where each cell is either water (W), desert (D), lowland (L) or highland (H). 
The map is surrounded by water.
- population: A list of dictionaries representing the initial population of animals on the island. 
Includes the following keys:
    - loc: The location of the cell where the animals are placed. 
    The location is given as a tuple of the x and y coordinates of the cell. 
    - Note that the animals cannot be placed in water.
    - pop: A list of dictionaries representing the animals in the population. 
    Includes the following keys:
        - species: The species of the animal. Can be either Herbivore or Carnivore.
        - age: The age of the animal. Must be a non-negative integer.
        - weight: The weight of the animal. Must be a positive integer.
  


## Futher development

### Tracking single animal
With being able to track a single animals you can
simulate how the rest of population will develop
and make a simulation forward in time.

### Track center of population 
Follow how the center of population moves on the island with time.

### Serialisation: using pickle
Saving and loading the BioSim instance to/from file using pickle. 
This will allow the user to save the state of the simulation and continue it later, 
or share the state with other users.

### Parallelization: using multiprocessing/threading
Using multiprocessing/threading under the simulation to help with visualization under the simulation.
### Bugs
- No known bugs

## License
MIT License
