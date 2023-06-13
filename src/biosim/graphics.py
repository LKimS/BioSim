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
    """Provides graphics support for RandVis."""

    def __init__(self, img_dir=None, img_name=None, img_fmt=None):
        """
        :param img_dir: directory for image files; no images if None
        :type img_dir: str
        :param img_name: beginning of name for image files
        :type img_name: str
        :param img_fmt: image file format suffix
        :type img_fmt: str
        """

        if img_name is None:
            img_name = _DEFAULT_GRAPHICS_NAME

        if img_dir is not None:
            self._img_base = os.path.join(img_dir, img_name)
        else:
            self._img_base = None

        self._img_fmt = img_fmt if img_fmt is not None else _DEFAULT_IMG_FORMAT

        self._img_ctr = 0
        self._img_step = 1

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
        self.population_line = None

        self.hist1_ax = None
        self.hist1_data = None
        self.hist2_ax = None
        self.hist2_data = None

        self.year_ax = None
        self.year_str = None
        self.year_text = None

        self.landscape_ax = None



    def update(self, step, population):
        """
        Updates graphics with current data and save to file if necessary.

        :param step: current time step
        :param sys_map: current system status (2d array)
        :param sys_mean: current mean value of system
        """


        self.update_population_graph(step, population)
        self.fig.canvas.flush_events()  # ensure every thing is drawn
        plt.pause(1e-6)  # pause required to pass control to GUI

        self._save_graphics(step)

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

    def setup(self, final_step, img_step):
        """
        Prepare graphics.

        Call this before calling :meth:`update()` for the first time after
        the final time step has changed.

        :param final_step: last time step to be visualised (upper limit of x-axis)
        :param img_step: interval between saving image to file
        """

        self._img_step = img_step

        # create new figure window
        if self.fig is None:
            img_size = (10, 10)
            self.fig = plt.figure(figsize=img_size)

        if self.ax is None:
            self.ax = self.fig.add_gridspec(3, 3)

            # Add left subplot for images created with imshow().
            # We cannot create the actual ImageAxis object before we know
            # the size of the image, so we delay its creation.
        if self.map_ax is None:
            self.map_ax = self.fig.add_subplot(self.ax[0, 1])
            self.map_img = None

            # Repeat for heatmap of the animals
        if self.herbivore_heatmap_ax is None:
            self.herbivore_heatmap_ax = self.fig.add_subplot(self.ax[1, 0])
            self.herbivore_heatmap_img = None

        if self.carnivore_heatmap_ax is None:
            self.carnivore_heatmap_ax = self.fig.add_subplot(self.ax[1, 1])
            self.carnivore_heatmap_img = None

        if self.population_ax is None:
            self.population_ax = self.fig.add_subplot(self.ax[1, :])
            self.population_ax.set_ylim(-0.05, 0.05)

        if self.population_line is None:
            population_plot = self.population_ax.plot(np.arange(0, final_step+1),
                                           np.full(final_step+1, np.nan))
            self.population_line = population_plot[0]
            self.population_ax.set_title('Population')
        else:
            x_data, y_data = self.population_line.get_data()
            x_new = np.arange(x_data[-1] + 1, final_step+1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self.population_line.set_data(np.hstack((x_data, x_new)),
                                         np.hstack((y_data, y_new)))

        if self.hist1_ax is None:
            self.hist1_ax = self.fig.add_subplot(self.ax[2, 0:2])
            self.hist1_data = None

        if self.hist2_ax is None:
            self.hist2_ax = self.fig.add_subplot(self.ax[2, 2])
            self.hist2_data = None



    def _update_system_map(self, sys_map):
        """Update the 2D-view of the system."""

        if self._img_axis is not None:
            self._img_axis.set_data(sys_map)
        else:
            self._img_axis = self._map_ax.imshow(sys_map,
                                                 interpolation='nearest',
                                                 vmin=-0.25, vmax=0.25)
            plt.colorbar(self._img_axis, ax=self._map_ax,
                         orientation='horizontal')

    def _update_mean_graph(self, step, mean):
        y_data = self._mean_line.get_ydata()
        y_data[step] = mean
        self._mean_line.set_ydata(y_data)

    def update_population_graph(self, step, population):
        y_data = self.population_line.get_ydata()
        y_data[step] = population
        self.population_line.set_ydata(y_data)

    def _save_graphics(self, step):
        """Saves graphics to file if file name given."""

        if self._img_base is None or step % self._img_step != 0:
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self._img_base,
                                                     num=self._img_ctr,
                                                     type=self._img_fmt))
        self._img_ctr += 1
