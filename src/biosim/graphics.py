"""
:mod:`randvis.graphics` provides graphics support for RandVis.

.. note::
   * This module requires the program ``ffmpeg`` or ``convert``
     available from `<https://ffmpeg.org>` and `<https://imagemagick.org>`.
   * You can also install ``ffmpeg`` using ``conda install ffmpeg``
   * You need to set the  :const:`_FFMPEG_BINARY` and :const:`_CONVERT_BINARY`
     constants below to the command required to invoke the programs
   * You need to set the :const:`_DEFAULT_FILEBASE` constant below to the
     directory and file-name start you want to use for the graphics output
     files.

"""

import matplotlib.pyplot as plt
import numpy as np
import subprocess
import os

# Update these variables to point to your ffmpeg and convert binaries
# If you installed ffmpeg using conda or installed both softwares in
# standard ways on your computer, no changes should be required.
_FFMPEG_BINARY = 'ffmpeg'
_MAGICK_BINARY = 'magick'

# update this to the directory and file-name beginning
# for the graphics files
_DEFAULT_GRAPHICS_DIR = os.path.join('../../../inf200-course-materials/june_block/examples/randvis_project', 'data')
_DEFAULT_GRAPHICS_NAME = 'dv'
_DEFAULT_IMG_FORMAT = 'png'
_DEFAULT_MOVIE_FORMAT = 'mp4'   # alternatives: mp4, gif


class Graphics:
    """Provides graphics support for BioSim."""

    default_ymax_animals = 1200
    default_cmax_animals = {'Herbivore': 100, 'Carnivore': 100}
    default_hist_specs = {'age': {'max': 60, 'delta': 2},
                          'weight': {'max': 80, 'delta': 2},
                          'fitness': {'max': 1.0, 'delta': 0.05}}
    def __init__(self, img_dir=None, img_name=None, img_fmt=None, img_years=None, live_visualization=True,
                 ymax_animals=1200, cmax_animals=None, hist_specs=None):
        """
        :param img_dir: directory for image files; no images if None
        :type img_dir: str
        :param img_name: beginning of name for image files
        :type img_name: str
        :param img_fmt: image file format suffix
        :type img_fmt: str
        :img_years: Years between visualizations saved to files (default: `vis_years`)
        :type img_years: int
        """

        if ymax_animals is not None:
            if ymax_animals < 0:
                raise ValueError(f'ymax_animals must be a positive number, not {ymax_animals}')
            self.ymax_animals = ymax_animals
        else:
            self.ymax_animals = self.default_ymax_animals



        if cmax_animals is not None:
            animals_species = list(self.default_cmax_animals.keys())
            self.cmax_animals = {}
            for key in cmax_animals:
                if key not in animals_species:
                    raise ValueError(f'Invalid key in cmax_animals: {key}. Valid keys are: {animals_species}')

                self.cmax_animals[key] = cmax_animals[key]
        else:
            self.cmax_animals = self.default_cmax_animals



        if hist_specs is not None:
            histograms = list(self.default_hist_specs.keys())
            self.hist_specs = self.default_hist_specs.copy()
            for key in hist_specs:
                if key not in histograms:
                    raise ValueError(f'Invalid key in hist_specs: {key}. Valid keys are: {histograms}')
                for spec in hist_specs[key]:
                    specs = list(self.default_hist_specs[key].keys())
                    if spec not in specs:
                        raise ValueError(f'Invalid key in hist_specs[{key}]: {spec}. Valid keys are: {specs}')
                    if hist_specs[key][spec] < 0:
                        value = hist_specs[key][spec]
                        raise ValueError(f'hist_specs[{key}][{spec}] must be a positive number, not {value}')

                    self.hist_specs[key][spec] = hist_specs[key][spec]
        else:
            self.hist_specs = self.default_hist_specs

        if img_name is None:
            img_name = _DEFAULT_GRAPHICS_NAME

        if img_dir is not None:
            self._img_base = os.path.join(img_dir, img_name)
        else:
            self._img_base = None

        if img_years is not None:
            self.img_years = img_years
        else:
            self.img_years = 1

        if img_fmt is not None:
            if img_fmt not in ['png', 'jpg']:
                raise ValueError(f'Invalid image format: {img_fmt}. Valid formats are: png, jpg')
            self._img_fmt = img_fmt
        else:
            self._img_fmt = _DEFAULT_IMG_FORMAT

        # Image counter
        self._img_ctr = 0

        # the following will be initialized by _setup_graphics
        self.fig = None
        self.ax = None
        self.map_ax = None
        self.map_img = None
        self.herbivore_heatmap_ax = None
        self.herbivore_heatmap_img = None
        self.carnivore_heatmap_ax = None
        self.carnivore_heatmap_img = None
        self.population_ax = None
        self.herbivore_population_line = None
        self.carnivore_population_line = None

        self.hist_age_ax = None
        self.hist_age_data = None
        self.hist_weight_ax = None
        self.hist_weight_data = None
        self.hist_fitness_ax = None
        self.hist_fitness_data = None

        self.year_ax = None
        self.year_str = None
        self.year_text = None

        self.landscape_ax = None

        self.live_visualization = live_visualization
        self.year = None



    def update(self, year,
               herbivore_population,
               carnivore_population,
               herbivore_dict_map ={},
               carnivore_dict_map={},
               herbivore_age_list=[],
               carnivore_age_list=[],
               herbivore_weight_list=[],
               carnivore_weight_list=[],
               herbivore_fitness_list=[],
               carnivore_fitness_list=[]):
        """
        Updates graphics with current data and save to file if necessary.

        :param year: current year
        :param sys_map: current system status (2d array)
        :param sys_mean: current mean value of system
        """

        self.year = year
        self.update_population_graph(year, herbivore_population, carnivore_population)
        self.update_hervibore_heatmap(herbivore_dict_map)
        self.update_carnivore_heatmap(carnivore_dict_map)
        self.update_histogram_age(herbivore_age_list, carnivore_age_list)
        self.update_histogram_weight(herbivore_weight_list, carnivore_weight_list)
        self.update_histogram_fitness(herbivore_fitness_list, carnivore_fitness_list)

        self.fig.canvas.flush_events()  # ensure every thing is drawn
        plt.pause(1e-6)  # pause required to pass control to GUI

        self._save_graphics(year)

    def make_movie(self, movie_fmt=None):
        """
        Creates MPEG4 movie from visualization images saved.

        .. :note:
            Requires ffmpeg for MP4 and magick for GIF

        The movie is stored as img_base + movie_fmt
        """

        if self._img_base is None:
            raise RuntimeError("No filename defined.")

        if movie_fmt is None:
            movie_fmt = _DEFAULT_MOVIE_FORMAT

        if movie_fmt == 'mp4':
            try:
                # Parameters chosen according to http://trac.ffmpeg.org/wiki/Encode/H.264,
                # section "Compatibility"
                subprocess.check_call([_FFMPEG_BINARY,
                                       '-i', '{}_%05d.png'.format(self._img_base),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(self._img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: ffmpeg failed with: {}'.format(err))
        elif movie_fmt == 'gif':
            try:
                subprocess.check_call([_MAGICK_BINARY,
                                       '-delay', '1',
                                       '-loop', '0',
                                       '{}_*.png'.format(self._img_base),
                                       '{}.{}'.format(self._img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: convert failed with: {}'.format(err))
        else:
            raise ValueError('Unknown movie format: ' + movie_fmt)

    def setup(self, map, final_step, img_step=1):
        """
        Prepare graphics.

        Call this before calling :meth:`update()` for the first time after
        the final time step has changed.

        :param final_step: last time step to be visualised (upper limit of x-axis)
        :param img_step: interval between saving image to file
        """

        self.img_years = img_step

        # create new figure window
        if self.fig is None:
            img_size = (10, 10)
            self.fig = plt.figure(figsize=img_size)
        # TODO: close fig
        if self.fig is not None and not self.live_visualization:
            plt.close(self.fig)

        if self.ax is None:
            self.ax = self.fig.add_gridspec(3, 3)

            # Add left subplot for images created with imshow().
            # We cannot create the actual ImageAxis object before we know
            # the size of the image, so we delay its creation.
        if self.map_ax is None:
            self.map_ax = self.fig.add_subplot(self.ax[0, 1])
            self.map_img = self.map_ax.imshow(map)
            self.bitmap = map
            self.map_ax.set_title('Map')
            self.map_ax.axis('off')

            # Repeat for heatmap of the animals
        if self.herbivore_heatmap_ax is None:
            self.herbivore_heatmap_ax = self.fig.add_subplot(self.ax[0, 0])
            self.herbivore_heatmap_img = None
            self.herbivore_heatmap_ax.set_title('Herbivores')
            self.herbivore_heatmap_ax.axis('off')

        if self.carnivore_heatmap_ax is None:
            self.carnivore_heatmap_ax = self.fig.add_subplot(self.ax[0, 2])
            self.carnivore_heatmap_ax.set_title('Carnivores')
            self.carnivore_heatmap_ax.axis('off')

        if self.population_ax is None:
            self.population_ax = self.fig.add_subplot(self.ax[1, :])
            self.population_ax.set_ylim(-0.05, 0.05)
            self.population_ax.set_xlim(0, 300)
            self.population_ax.set_ylim(0, self.ymax_animals)
            self.population_ax.set_title('Population')
            self.population_ax.set_xlabel('Year')

        if self.herbivore_population_line is None:
            herbivore_population_plot = self.population_ax.plot(np.arange(0, final_step+1),
                                           np.full(final_step+1, np.nan), color="blue")
            self.herbivore_population_line = herbivore_population_plot[0]

        else:
            x_data, y_data = self.herbivore_population_line.get_data()
            x_new = np.arange(x_data[-1] + 1, final_step+1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self.herbivore_population_line.set_data(np.hstack((x_data, x_new)),
                                                        np.hstack((y_data, y_new)))

        if self.carnivore_population_line is None:
            carnivore_population_plot = self.population_ax.plot(np.arange(0, final_step+1),
                                           np.full(final_step+1, np.nan), color="red")
            self.carnivore_population_line = carnivore_population_plot[0]
        else:
            x_data, y_data = self.carnivore_population_line.get_data()
            x_new = np.arange(x_data[-1] + 1, final_step+1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self.carnivore_population_line.set_data(np.hstack((x_data, x_new)),
                                                        np.hstack((y_data, y_new)))

        if self.hist_age_ax is None:
            self.hist_age_ax = self.fig.add_subplot(self.ax[2, 0:1])

            self.age_bin_max = self.hist_specs["age"]["max"]
            self.age_bin_width = self.hist_specs["age"]["delta"]
            self.age_y_max = .3

            self.age_bin_edges = np.arange(0, self.age_bin_max + self.age_bin_width / 2, self.age_bin_width)
            self.age_hist_counts = np.zeros_like(self.age_bin_edges[:-1], dtype=float)
            self.age_herbivore_hist = self.hist_age_ax.stairs(self.age_hist_counts, self.age_bin_edges, color='blue',
                                                              lw=2, label='Hebivore')
            self.age_carnivore_hist = self.hist_age_ax.stairs(self.age_hist_counts, self.age_bin_edges, color='red',
                                                                lw=2, label='Carnivore')
            self.hist_age_ax.set_ylim(0, self.age_y_max)

        if self.hist_weight_ax is None:
            self.hist_weight_ax = self.fig.add_subplot(self.ax[2, 1])

            self.weight_bin_max = self.hist_specs["weight"]["max"]
            self.weight_bin_width = self.hist_specs["weight"]["delta"]
            self.weight_y_max = .3

            self.weight_bin_edges = np.arange(0, self.weight_bin_max + self.weight_bin_width / 2, self.weight_bin_width)
            self.weight_hist_counts = np.zeros_like(self.weight_bin_edges[:-1], dtype=float)
            self.weight_herbivore_hist = self.hist_weight_ax.stairs(self.weight_hist_counts, self.weight_bin_edges, color='blue',
                                                                lw=2, label='Hebivore')
            self.weight_carnivore_hist = self.hist_weight_ax.stairs(self.weight_hist_counts, self.weight_bin_edges, color='red',
                                                                lw=2, label='Carnivore')
            self.hist_weight_ax.set_ylim(0, self.weight_y_max)

        if self.hist_fitness_ax is None:
            self.hist_fitness_ax = self.fig.add_subplot(self.ax[2, 2])

            self.fitness_bin_max = self.hist_specs["fitness"]["max"]
            self.fitness_bin_width = self.hist_specs["fitness"]["delta"]
            self.fitness_y_max =20

            self.fitness_bin_edges = np.arange(0, self.fitness_bin_max + self.fitness_bin_width / 2, self.fitness_bin_width)
            self.fitness_hist_counts = np.zeros_like(self.fitness_bin_edges[:-1], dtype=float)
            self.fitness_herbivore_hist = self.hist_fitness_ax.stairs(self.fitness_hist_counts, self.fitness_bin_edges, color='blue',
                                                                lw=2, label='Hebivore')
            self.fitness_carnivore_hist = self.hist_fitness_ax.stairs(self.fitness_hist_counts, self.fitness_bin_edges, color='red',
                                                                lw=2, label='Carnivore')
            self.hist_fitness_ax.set_ylim(0, self.fitness_y_max)





    def update_population_graph(self, year, herbivore_population, carnivore_population):
        """Update the graph of the population.
        Parameters
        ----------
        year
        population

        Returns
        -------

        """
        if year > 300:
            self.population_ax.set_xlim(year - 300, year)


        herbivore_y_data = self.herbivore_population_line.get_ydata()
        herbivore_y_data[year] = herbivore_population
        self.herbivore_population_line.set_ydata(herbivore_y_data)

        carnivore_y_data = self.carnivore_population_line.get_ydata()
        carnivore_y_data[year] = carnivore_population
        self.carnivore_population_line.set_ydata(carnivore_y_data)

        y_val = [num for num in herbivore_y_data + carnivore_y_data if not np.isnan(num)]

        #y_max = max(y_val + [self.ymax_animals])
        #self.population_ax.set_ylim(0, y_max*1.1)

    def update_hervibore_heatmap(self, herbivore_dict_map):
        if self.herbivore_heatmap_img is None:

            dimx = self.bitmap.shape[0]
            dimy = self.bitmap.shape[1]

            self.herbivore_map = np.zeros((dimx, dimy))

            for location, population_history in herbivore_dict_map.items():
                x = location[0] - 1
                y = location[1] - 1
                self.herbivore_map[x][y] = population_history
            cmax = self.cmax_animals["Herbivore"]
            self.herbivore_heatmap_img = self.herbivore_heatmap_ax.imshow(self.herbivore_map,
                                                                           interpolation='nearest',
                                                                           vmin=0, vmax=cmax, cmap="YlGnBu")
            plt.colorbar(self.herbivore_heatmap_img, ax=self.herbivore_heatmap_ax)
        else:
            for location, population_history in herbivore_dict_map.items():
                x = location[0] - 1
                y = location[1] - 1
                self.herbivore_map[x][y] = population_history
            self.herbivore_heatmap_img.set_data(self.herbivore_map)

    def update_carnivore_heatmap(self, carnivore_dict_map):
        if self.carnivore_heatmap_img is None:

            dimx = self.bitmap.shape[0]
            dimy = self.bitmap.shape[1]

            self.carnivore_map = np.zeros((dimx, dimy))

            for key, value in carnivore_dict_map.items():
                x = key[0] - 1
                y = key[1] - 1
                self.carnivore_map[x][y] = value
            cmax = self.cmax_animals["Carnivore"]
            self.carnivore_heatmap_img = self.carnivore_heatmap_ax.imshow(self.carnivore_map,
                                                                           interpolation='nearest',
                                                                           vmin=0, vmax=cmax, cmap="YlOrBr")
            plt.colorbar(self.carnivore_heatmap_img, ax=self.carnivore_heatmap_ax)
        else:
            for key, value in carnivore_dict_map.items():
                x = key[0] - 1
                y = key[1] - 1
                self.carnivore_map[x][y] = value
            self.carnivore_heatmap_img.set_data(self.carnivore_map)

    def update_histogram_age(self, herbivore_age_list, carnivore_age_list):

        if herbivore_age_list is not None:
            hist_counts_age_herbivore, _ = np.histogram(herbivore_age_list, bins=self.age_bin_edges, density=True)
            self.age_herbivore_hist.set_data(hist_counts_age_herbivore)

        if carnivore_age_list is not None:
            hist_counts_age_carnivore, _ = np.histogram(carnivore_age_list, bins=self.age_bin_edges, density=True)
            self.age_carnivore_hist.set_data(hist_counts_age_carnivore)


    def update_histogram_weight(self, herbivore_weight_list, carnivore_weight_list):

        if herbivore_weight_list is not None:
            hist_counts_weight_herbivore, _ = np.histogram(herbivore_weight_list, bins=self.weight_bin_edges, density=True)
            self.weight_herbivore_hist.set_data(hist_counts_weight_herbivore)

        if carnivore_weight_list is not None:
            hist_counts_weight_carnivore, _ = np.histogram(carnivore_weight_list, bins=self.weight_bin_edges, density=True)
            self.weight_carnivore_hist.set_data(hist_counts_weight_carnivore)

    def update_histogram_fitness(self, herbivore_fitness_list, carnivore_fitness_list):

        if herbivore_fitness_list is not None:
            hist_counts_fitness_herbivore, _ = np.histogram(herbivore_fitness_list, bins=self.fitness_bin_edges, density=True)
            self.fitness_herbivore_hist.set_data(hist_counts_fitness_herbivore)

        if carnivore_fitness_list is not None:
            hist_counts_fitness_carnivore, _ = np.histogram(carnivore_fitness_list, bins=self.fitness_bin_edges, density=True)
            self.fitness_carnivore_hist.set_data(hist_counts_fitness_carnivore)








    def _save_graphics(self, step):
        """Saves graphics to file if file name given."""

        if self._img_base is None or step % self.img_years != 0:
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self._img_base,
                                                     num=self._img_ctr,
                                                     type=self._img_fmt))
        self._img_ctr += 1
