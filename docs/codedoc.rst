Code documentation
===================

Simulation
-------------
The simulation is run by the BioSim- and Graphics-class.
BioSim simulates the ecosystem on the Island, Graphics visualizes the data from the simulation.
If you run the simulation once, you simulate one year.

BioSim
+++++++
BioSim class is the top-level interface to BioSim package. It implements a complete simulation
of the ecosystem. Choose between multiple different parameters to adjust your simulation and preferred output.

.. autoclass:: biosim.simulation.BioSim
    :inherited-members:

Graphics
++++++++
Graphics provides graphics support for BioSim.
This module was inspired by RandVis package by Hans Ekkehard Plesser

* This module requires the program ``ffmpeg`` or ``convert`` available from `<https://ffmpeg.org>` and `<https://imagemagick.org>`.
* You can also install ``ffmpeg`` using ``conda install ffmpeg``
* You need to set the  :const:`_FFMPEG_BINARY` and :const:`_CONVERT_BINARY` constants below to the command required to invoke the programs
* You need to set the :const:`_DEFAULT_FILEBASE` constant below to the directory and file-name start you want to use for the graphics output files.


.. autoclass:: biosim.graphics.Graphics
    :inherited-members:

Island
----------

.. automodule:: biosim.island
    :inherited-members:

Cell
----------
Hei hei

.. autoclass:: biosim.cell.Water
    :inherited-members:

.. autoclass:: biosim.cell.Desert
    :inherited-members:

.. autoclass:: biosim.cell.Lowland
    :inherited-members:

.. autoclass:: biosim.cell.Highland
    :inherited-members:

Animals
----------

.. autoclass:: biosim.animals.Herbivore
    :inherited-members:

.. autoclass:: biosim.animals.Carnivore
    :inherited-members:

