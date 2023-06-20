.. biosim-u22-kim-mathias documentation master file, created by
   sphinx-quickstart on Thu Jun 15 12:47:52 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Biosim - A model of the ecosystem Rossumøya
==================================================

Background
-----------------
The Environmental Protection Agency of Pylandia (EPAP)
established research groups to develop a simulation of
the population dynamics of Rossumøya. The long term goal
is to use the simulation to preserve Rossumøya as a nautre
park for futher generations.

Project mandate
---------------
Create a simulation of Rossumøya with animals living
and migration on the island through generations.

For more information follow the link:

Development Process
-------------------
The development process started with understanding all
principles of animals lifecycle the island.
All information where allocated to GitLab issueboard, and to
a hierarchic map for our code. The code is driven by test-development
and coding simultaneously.

To get going quickly first step is to settle inputs and outputs from
each level in the hierarchy. Second step is to make de code separate,
and third step is to make the code work together. With more and more
features the code gets more and more complex. At one point we
saw a big performance gain by changing the code-structure. After reorganizing
the code we saw a big performance gain.

With following the milestones and using the issuebord we managed to keep
up progression each day. Two days we got really stuck on some bugs that
where hard to find.

At our first profiling, we saw that our code were preforming very well.
By only looping on habitat areas at the island we made the code faster,
the drawback is that the code don't work with animals that lives in the ocean.
Another smart idea was to only let the animals eat if they have something
to eat in that cell. This makes the code a lot faster!


For more information about the documentation, see the following sections bellow.



.. toctree::
   :maxdepth: 3
   :caption: Contents:


   home

   codedoc

   examples

   further




