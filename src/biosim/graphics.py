

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
_DEFAULT_GRAPHICS_NAME = 'dv'
_DEFAULT_IMG_FORMAT = 'png'
_DEFAULT_MOVIE_FORMAT = 'mp4'  # alternatives: gif


class Graphics:
    """
    Visualization of island
    """


    # Default values for visualization parameters
    default_ymax_animals = 30000
    default_cmax_animals = {'Herbivore': 140, 'Carnivore': 100}
    default_hist_specs = {'age': {'max': 60, 'delta': 5},
                          'weight': {'max': 80, 'delta': 5},
                          'fitness': {'max': 1.0, 'delta': 0.1}}
    age_y_max = .2
    weight_y_max = .15
    fitness_y_max = .3
    hist_update_y_ax = 48

    rgb_value = {'W': (0.13, 0.00, 1.00),  # blue
                 'L': (0.00, 0.62, 0.00),  # dark green
                 'H': (0.20, 1.00, 0.42),  # light green
                 'D': (1.00, 1.00, 0.40)}  # light yellow

    def __init__(self, img_dir=None, img_name=None, img_fmt=None, img_years=None, vis_years=0,
                 ymax_animals=1200, cmax_animals=None, hist_specs=None):
        """
        Initialization up a new visualization object.

        :param img_dir: directory for image files; no images if None
        :type img_dir: str
        :param img_name: beginning of name for image files
        :type img_name: str
        :param img_fmt: image file format suffix
        :type img_fmt: str
        :img_years: Years between visualizations saved to files (default: `vis_years`)
        :type img_years: int

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

        # check if ymax_animals is a positive number
        if ymax_animals is not None:
            if ymax_animals < 0:
                raise ValueError(f'ymax_animals must be a positive number, not {ymax_animals}')
            self.ymax_animals = ymax_animals
        else:
            self.ymax_animals = self.default_ymax_animals

        if vis_years is not None:
            if vis_years < 0 or type(vis_years) != type(int()):
                print(type(vis_years))
                raise ValueError(f'vis_years must be a positive integer, not {vis_years}')

            self.vis_years = vis_years

        if vis_years == 0:
            return

        # check if cmax_animals is a dictionary with valid keys
        if cmax_animals is not None:
            animals_species = list(self.default_cmax_animals.keys())
            self.cmax_animals = {}
            for key in cmax_animals:
                if key not in animals_species:
                    raise ValueError(f'Invalid key in cmax_animals: {key}. Valid keys are: {animals_species}')

                self.cmax_animals[key] = cmax_animals[key]
        else:
            self.cmax_animals = self.default_cmax_animals

        # check if hist_specs is a dictionary with valid keys and values
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
        # Frame counter
        self._frame_ctr = 0

        # the following will be initialized by _setup_graphics
        self._fig = None
        self._ax = None
        self._map_ax = None
        self._map_img = None
        self._dim_x = None
        self._dim_y = None
        self._herbivore_heatmap_ax = None
        self._herbivore_heatmap_img = None
        self._carnivore_heatmap_ax = None
        self._carnivore_heatmap_img = None
        self._population_ax = None
        self.herbivore_population_line = None
        self._carnivore_population_line = None

        self._hist_age_ax = None
        self._hist_age_data = None
        self._hist_weight_ax = None
        self._hist_weight_data = None
        self._hist_fitness_ax = None
        self._hist_fitness_data = None

        self._year_ax = None
        self._year_str = None
        self._year_text = None

        self._landscape_ax = None

        self.year = None
        self.final_year = None

    def update(self, year,
               herbivore_population,
               carnivore_population,
               herbivore_dict_map={},
               carnivore_dict_map={},
               herbivore_age_list=None,
               carnivore_age_list=None,
               herbivore_weight_list=None,
               carnivore_weight_list=None,
               herbivore_fitness_list=None,
               carnivore_fitness_list=None):
        """
        Updates graphics with current data and save to file if necessary.

        :param year: current year.
        :type year: int
        :param herbivore_population: current herbivore population.
        :type herbivore_population: int
        :param carnivore_population: current carnivore population.
        :type carnivore_population: int
        :param herbivore_dict_map: current herbivore population distribution.
        :type herbivore_dict_map: dict
        :param carnivore_dict_map: current carnivore population distribution.
        :type carnivore_dict_map: dict
        :param herbivore_age_list: current herbivore age distribution.
        :type herbivore_age_list: list
        :param carnivore_age_list: current carnivore age distribution.
        :type carnivore_age_list: list
        :param herbivore_weight_list: current herbivore weight distribution.
        :type herbivore_weight_list: list
        :param carnivore_weight_list: current carnivore weight distribution.
        :type carnivore_weight_list: list
        :param herbivore_fitness_list: current herbivore fitness distribution.
        :type herbivore_fitness_list: list
        :param carnivore_fitness_list: current carnivore fitness distribution.
        :type carnivore_fitness_list: list
        """

        self.year = year
        self._update_year_counter(year)
        self._update_population_graph(year, herbivore_population, carnivore_population)
        self._update_herbivore_heatmap(herbivore_dict_map)
        self._update_carnivore_heatmap(carnivore_dict_map)
        self._update_histogram_age(herbivore_age_list, carnivore_age_list)
        self._update_histogram_weight(herbivore_weight_list, carnivore_weight_list)
        self._update_histogram_fitness(herbivore_fitness_list, carnivore_fitness_list)

        self._fig.canvas.flush_events()  # ensure every thing is drawn
        plt.pause(1e-6)  # pause required to pass control to GUI

        self._frame_ctr += 1
        self._save_graphics(year)

    def make_movie(self, movie_fmt=None):
        """
        Creates MPEG4 movie from visualization images saved.

        :param movie_fmt: Video format, either mp4 (default) or gif.
        :type movie_fmt: str

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

    def setup(self, geography, final_year, vis_years=1):
        """
        Prepare graphics with population history, histograms and heatmaps for the island.

        :param geography: A list of lists containing the landscape. From Island.processed_map
        :type geography: list
        :param final_year: last time step to be visualised (upper limit of x-axis)
        :type final_year: int


        .. note::
            Call this before calling :meth:`update()` for the first time after
            the final time step has changed.


        """

        self.final_year = final_year

        # create new figure window
        if self._fig is None:
            scale_factor = .8
            img_size = (16 * scale_factor, 10 * scale_factor)
            self._fig = plt.figure(figsize=img_size)

        if self._ax is None:
            self._ax = self._fig.add_gridspec(12, 3)

        # Add year counter in upper left corner
        if self._year_ax is None:
            self._year_ax = self._fig.add_axes([.2, .9, .2, .06])  # llx, lly, w, h
            self.year_counter = None
            self._year_ax.axis('off')

        # Add landscape patches

        if self._landscape_ax is None:
            self._landscape_ax = self._fig.add_axes([.4, .01, .22, .09])  # llx, lly, w, h
            self._landscape_ax.axis('off')

            self._landscape_ax.add_patch(plt.Rectangle((0, .6), 0.2, 0.4, edgecolor='none',
                                                       facecolor=self.rgb_value['W']))
            self._landscape_ax.text(.22, 0.7, 'Water', transform=self._landscape_ax.transAxes)

            self._landscape_ax.add_patch(plt.Rectangle((0, .0), 0.2, 0.4, edgecolor='none',
                                                       facecolor=self.rgb_value['D']))
            self._landscape_ax.text(.22, 0.16, 'Desert', transform=self._landscape_ax.transAxes)

            self._landscape_ax.add_patch(plt.Rectangle((.5, .6), 0.2, 0.4, edgecolor='none',
                                                       facecolor=self.rgb_value['L']))
            self._landscape_ax.text(.73, .7, 'Lowland', transform=self._landscape_ax.transAxes)

            self._landscape_ax.add_patch(plt.Rectangle((0.5, .0), 0.2, 0.4, edgecolor='none',
                                                       facecolor=self.rgb_value['H']))
            self._landscape_ax.text(.73, 0.16, 'Highland', transform=self._landscape_ax.transAxes)

        # Add left subplot for images created with imshow().
        # We cannot create the actual ImageAxis object before we know
        # the size of the image, so we delay its creation.
        if self._map_ax is None:
            color_map = [[self.rgb_value[landscape] for landscape in row] for row in geography]
            self._dim_x = len(geography)
            self._dim_y = len(geography[0])
            self._map_ax = self._fig.add_subplot(self._ax[8:, 1])
            self._map_img = self._map_ax.imshow(color_map)
            self.geography = geography
            self._map_ax.set_title('Map')
            self._map_ax.axis('off')

            self._map_title_ax = self._fig.add_axes([0, 0.12, .1, .25])  # llx, lly, w, h
            self._map_title_ax.text(0.5, 0.5, 'Population\ndensity', horizontalalignment='center',
                                    verticalalignment='center', fontsize=15, rotation=45)
            self._map_title_ax.axis('off')

        # Repeat for heatmap of the animals
        if self._herbivore_heatmap_ax is None:
            self._herbivore_heatmap_ax = self._fig.add_subplot(self._ax[8:, 0])
            self._herbivore_heatmap_img = None
            self._herbivore_heatmap_ax.set_title('Herbivores')
            self._herbivore_heatmap_ax.axis('off')

        if self._carnivore_heatmap_ax is None:
            self._carnivore_heatmap_ax = self._fig.add_subplot(self._ax[8:, 2])
            self._carnivore_heatmap_ax.set_title('Carnivores')
            self._carnivore_heatmap_ax.axis('off')

        # Setting up the population plot
        if self._population_ax is None:
            self._population_ax = self._fig.add_subplot(self._ax[0:3, :])
            self._population_ax.set_ylim(-0.05, 0.05)
            self._population_ax.set_ylim(0, self.ymax_animals)
            # self._population_ax.set_title('Population')
            self._population_ax.set_xlabel('Year', loc='right')

            self._population_title_ax = self._fig.add_axes([0, .7, .1, .18])  # llx, lly, w, h
            self._population_title_ax.text(0.5, 0.5, 'Population\nHistory', horizontalalignment='center',
                                           verticalalignment='center', fontsize=15, rotation=45)
            self._population_title_ax.axis('off')

        self._population_ax.set_xlim(0, final_year)
        xdata = np.arange(0, final_year + 1, self.vis_years)

        if self.herbivore_population_line is None:

            herbivore_population_plot = self._population_ax.plot(xdata,
                                                                 np.full(len(xdata), np.nan),
                                                                 color="blue", label="Herbivores")
            self.herbivore_population_line = herbivore_population_plot[0]

        else:
            x_data, y_data = self.herbivore_population_line.get_data()
            x_new = np.arange(x_data[-1] + self.vis_years, final_year + 1, self.vis_years)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self.herbivore_population_line.set_data(np.hstack((x_data, x_new)),
                                                        np.hstack((y_data, y_new)))

        if self._carnivore_population_line is None:
            carnivore_population_plot = self._population_ax.plot(xdata,
                                                                 np.full(len(xdata), np.nan),
                                                                 color="red", label="Carnivores")
            self._carnivore_population_line = carnivore_population_plot[0]
        else:
            x_data, y_data = self._carnivore_population_line.get_data()
            x_new = np.arange(x_data[-1] + self.vis_years, final_year + 1, self.vis_years)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self._carnivore_population_line.set_data(np.hstack((x_data, x_new)),
                                                         np.hstack((y_data, y_new)))

        # Setting up the histogram
        if self._hist_age_ax is None:
            self._hist_age_ax = self._fig.add_subplot(self._ax[4:7, 0])
            self._hist_age_ax.set_title('Age distribution')

            self.age_bin_max = self.hist_specs["age"]["max"]
            self.age_bin_width = self.hist_specs["age"]["delta"]

            self.age_bin_edges = np.arange(0, self.age_bin_max + self.age_bin_width / 2, self.age_bin_width)
            self.age_hist_counts = np.zeros_like(self.age_bin_edges[:-1], dtype=float)
            self.age_herbivore_hist = self._hist_age_ax.stairs(self.age_hist_counts, self.age_bin_edges, color='blue',
                                                               lw=2, label='Hebivore')
            self.age_carnivore_hist = self._hist_age_ax.stairs(self.age_hist_counts, self.age_bin_edges, color='red',
                                                               lw=2, label='Carnivore')
            self._hist_age_ax.set_ylim(0, self.age_y_max)

        if self._hist_weight_ax is None:
            self._hist_weight_ax = self._fig.add_subplot(self._ax[4:7, 1])
            self._hist_weight_ax.set_title('Weight distribution')

            self.weight_bin_max = self.hist_specs["weight"]["max"]
            self.weight_bin_width = self.hist_specs["weight"]["delta"]
            self.weight_y_max = .15

            self.weight_bin_edges = np.arange(0, self.weight_bin_max + self.weight_bin_width / 2, self.weight_bin_width)
            self.weight_hist_counts = np.zeros_like(self.weight_bin_edges[:-1], dtype=float)
            self.weight_herbivore_hist = self._hist_weight_ax.stairs(self.weight_hist_counts, self.weight_bin_edges,
                                                                     color='blue',
                                                                     lw=2, label='Hebivore')
            self.weight_carnivore_hist = self._hist_weight_ax.stairs(self.weight_hist_counts, self.weight_bin_edges,
                                                                     color='red',
                                                                     lw=2, label='Carnivore')
            self._hist_weight_ax.set_ylim(0, self.weight_y_max)

            plt.legend(bbox_to_anchor=(.36, .895), loc="lower left",
                       bbox_transform=self._fig.transFigure, ncol=2, fontsize=15)

            self._hist_title_ax = self._fig.add_axes([0, .44, .1, .18])  # llx, lly, w, h
            self._hist_title_ax.text(0.5, 0.5, 'Normalized\nhistograms', horizontalalignment='center',
                                     verticalalignment='center', fontsize=15, rotation=45)
            self._hist_title_ax.axis('off')

        if self._hist_fitness_ax is None:
            self._hist_fitness_ax = self._fig.add_subplot(self._ax[4:7, 2])
            self._hist_fitness_ax.set_title('Fitness distribution')

            self.fitness_bin_max = self.hist_specs["fitness"]["max"]
            self.fitness_bin_width = self.hist_specs["fitness"]["delta"]
            self.fitness_y_max = .6

            self.fitness_bin_edges = np.arange(0, self.fitness_bin_max + self.fitness_bin_width / 2,
                                               self.fitness_bin_width)
            self.fitness_hist_counts = np.zeros_like(self.fitness_bin_edges[:-1], dtype=float)
            self.fitness_herbivore_hist = self._hist_fitness_ax.stairs(self.fitness_hist_counts, self.fitness_bin_edges,
                                                                       color='blue',
                                                                       lw=2, label='Hebivore')
            self.fitness_carnivore_hist = self._hist_fitness_ax.stairs(self.fitness_hist_counts, self.fitness_bin_edges,
                                                                       color='red',
                                                                       lw=2, label='Carnivore')
            self._hist_fitness_ax.set_ylim(0, self.fitness_y_max)

    def _update_year_counter(self, year):
        """Update the year counter.

        :param year: int
        """
        year_txt = f"Year: {year}"
        if self.year_counter is None:
            self.year_counter = self._year_ax.text(0.5, 0.5, year_txt, horizontalalignment='center',
                                                   verticalalignment='center', fontsize=20)
        else:
            self.year_counter.set_text(f"Year: {year}")

    def _update_population_graph(self, year, herbivore_population, carnivore_population):
        """
        Update the population graph.

        :param year: Current year
        :type year: int
        :param herbivore_population: Current herbivore population
        :type herbivore_population: int
        :param carnivore_population: Current carnivore population
        :type carnivore_population: int
        """

        idx = year // self.vis_years
        herbivore_y_data = self.herbivore_population_line.get_ydata()
        herbivore_y_data[idx] = herbivore_population
        self.herbivore_population_line.set_ydata(herbivore_y_data)

        carnivore_y_data = self._carnivore_population_line.get_ydata()
        carnivore_y_data[idx] = carnivore_population
        self._carnivore_population_line.set_ydata(carnivore_y_data)

    def _update_herbivore_heatmap(self, herbivore_dict_map):
        """
        Update the herbivore heatmap.

        :param herbivore_dict_map: Dictionary with herbivore population history
        :type herbivore_dict_map: dict
        """
        if self._herbivore_heatmap_img is None:

            self.herbivore_map = np.zeros((self._dim_x, self._dim_y))

            for location, population_history in herbivore_dict_map.items():
                x = location[0] - 1
                y = location[1] - 1
                self.herbivore_map[x][y] = population_history
            cmax = self.cmax_animals["Herbivore"]
            self._herbivore_heatmap_img = self._herbivore_heatmap_ax.imshow(self.herbivore_map,
                                                                            interpolation='nearest',
                                                                            vmin=0, vmax=cmax, cmap="YlGnBu")
            plt.colorbar(self._herbivore_heatmap_img, ax=self._herbivore_heatmap_ax, location='left', pad=.05)
        else:
            for location, population_history in herbivore_dict_map.items():
                x = location[0] - 1
                y = location[1] - 1
                self.herbivore_map[x][y] = population_history
            self._herbivore_heatmap_img.set_data(self.herbivore_map)

    def _update_carnivore_heatmap(self, carnivore_dict_map):
        """
        Update the carnivore heatmap.

        :param carnivore_dict_map: Dictionary with carnivore population history
        :type carnivore_dict_map: dict
        """
        if self._carnivore_heatmap_img is None:

            self.carnivore_map = np.zeros((self._dim_x, self._dim_y))

            for key, value in carnivore_dict_map.items():
                x = key[0] - 1
                y = key[1] - 1
                self.carnivore_map[x][y] = value
            cmax = self.cmax_animals["Carnivore"]
            self._carnivore_heatmap_img = self._carnivore_heatmap_ax.imshow(self.carnivore_map,
                                                                            interpolation='nearest',
                                                                            vmin=0, vmax=cmax, cmap="YlOrBr")
            plt.colorbar(self._carnivore_heatmap_img, ax=self._carnivore_heatmap_ax)
        else:
            for key, value in carnivore_dict_map.items():
                x = key[0] - 1
                y = key[1] - 1
                self.carnivore_map[x][y] = value
            self._carnivore_heatmap_img.set_data(self.carnivore_map)

    def _update_histogram_age(self, herbivore_age_list, carnivore_age_list):
        """
        Update the age histogram.

        :param herbivore_age_list: List of herbivore ages
        :type herbivore_age_list: list
        :param carnivore_age_list: List of carnivore ages
        :type carnivore_age_list: list
        """

        if herbivore_age_list is not None and herbivore_age_list != []:
            hist_counts_age_herbivore, _ = np.histogram(herbivore_age_list, bins=self.age_bin_edges, density=True)
            hist_counts_age_herbivore_norm = hist_counts_age_herbivore / np.sum(hist_counts_age_herbivore)

            # Update y-axis
            if self._frame_ctr % self.hist_update_y_ax == 0:
                y_max = max(self.age_y_max, max(hist_counts_age_herbivore_norm) * 1.1)
                self._hist_age_ax.set_ylim([0, y_max])

            self.age_herbivore_hist.set_data(hist_counts_age_herbivore_norm)

        if carnivore_age_list is not None and carnivore_age_list != []:
            hist_counts_age_carnivore, _ = np.histogram(carnivore_age_list, bins=self.age_bin_edges, density=True)
            hist_counts_age_carnivore_norm = hist_counts_age_carnivore / np.sum(hist_counts_age_carnivore)

            if self._frame_ctr % self.hist_update_y_ax == 0:
                y_max = max(self.age_y_max, max(hist_counts_age_herbivore_norm) * 1.1,
                            max(hist_counts_age_carnivore_norm) * 1.1)
                self._hist_age_ax.set_ylim([0, y_max])

            self.age_carnivore_hist.set_data(hist_counts_age_carnivore_norm)

    def _update_histogram_weight(self, herbivore_weight_list, carnivore_weight_list):
        """
        Update the weight histogram.

        :param herbivore_weight_list: List of herbivore weights
        :type herbivore_weight_list: list
        :param carnivore_weight_list: List of carnivore weights
        :type carnivore_weight_list: list
        """

        if herbivore_weight_list is not None and herbivore_weight_list != []:
            hist_counts_weight_herbivore, _ = np.histogram(herbivore_weight_list, bins=self.weight_bin_edges,
                                                           density=True)
            hist_counts_weight_herbivore_norm = hist_counts_weight_herbivore / np.sum(hist_counts_weight_herbivore)

            if self._frame_ctr % self.hist_update_y_ax == 0:
                y_max = max(self.weight_y_max, max(hist_counts_weight_herbivore_norm) * 1.1)
                self._hist_weight_ax.set_ylim([0, y_max])

            self.weight_herbivore_hist.set_data(hist_counts_weight_herbivore_norm)

        if carnivore_weight_list is not None and carnivore_weight_list != []:
            hist_counts_weight_carnivore, _ = np.histogram(carnivore_weight_list, bins=self.weight_bin_edges,
                                                           density=True)
            hist_counts_weight_carnivore_norm = hist_counts_weight_carnivore / np.sum(hist_counts_weight_carnivore)

            if self._frame_ctr % self.hist_update_y_ax == 0:
                y_max = max(self.weight_y_max, max(hist_counts_weight_herbivore_norm) * 1.1,
                            max(hist_counts_weight_carnivore_norm) * 1.1)

                self._hist_weight_ax.set_ylim([0, y_max])

            self.weight_carnivore_hist.set_data(hist_counts_weight_carnivore_norm)

    def _update_histogram_fitness(self, herbivore_fitness_list, carnivore_fitness_list):
        """
        Update the histogram of fitness for herbivores and carnivores.

        .. note::

            Normalized the histogram with the help from:
            https://stackoverflow.com/questions/21532667/numpy-histogram-cumulative-density-does-not-sum-to-1

        :param herbivore_fitness_list: List of herbivore fitness
        :type herbivore_fitness_list: list
        :param carnivore_fitness_list: List of carnivore fitness

"""

        if herbivore_fitness_list is not None and herbivore_fitness_list != []:
            hist_counts_fitness_herbivore, _ = np.histogram(herbivore_fitness_list,
                                                            bins=self.fitness_bin_edges, density=True)
            hist_counts_fitness_herbivore_norm = hist_counts_fitness_herbivore / np.sum(hist_counts_fitness_herbivore)

            if self._frame_ctr % self.hist_update_y_ax == 0:
                y_max = max(self.fitness_y_max, max(hist_counts_fitness_herbivore_norm) * 1.1)
                self._hist_fitness_ax.set_ylim([0, y_max])

            self.fitness_herbivore_hist.set_data(hist_counts_fitness_herbivore_norm)

        if carnivore_fitness_list is not None and carnivore_fitness_list != []:
            hist_counts_fitness_carnivore, _ = np.histogram(carnivore_fitness_list,
                                                            bins=self.fitness_bin_edges, density=True)
            hist_counts_fitness_carnivore_norm = hist_counts_fitness_carnivore / np.sum(hist_counts_fitness_carnivore)

            if self._frame_ctr % self.hist_update_y_ax == 0:
                y_max = max(self.fitness_y_max,
                            max(hist_counts_fitness_herbivore_norm) * 1.1,
                            max(hist_counts_fitness_carnivore_norm) * 1.1)
                self._hist_fitness_ax.set_ylim([0, y_max])

            self.fitness_carnivore_hist.set_data(hist_counts_fitness_carnivore_norm)

    def _save_graphics(self, year):
        """Saves graphics to file if file name given.

        :param year: Year of simulation
        :type year: int
        """

        # check if file name is given and if year is a multiple of img_years
        if self._img_base is None or year % self.img_years != 0:
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self._img_base,
                                                     num=self._img_ctr,
                                                     type=self._img_fmt))
        self._img_ctr += 1
