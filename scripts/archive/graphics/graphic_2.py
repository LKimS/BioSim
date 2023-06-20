from biosim.island import Island
import matplotlib.pyplot as plt
import random
SIM_YEARS = 3
"""
https://blog.finxter.com/matplotlib-how-to-change-subplot-sizes/
"""

geogr = """\
           WWWWWWWWWWWWWWWWWWWWW
           WHHHHHLLLLWWLLLLLLLWW
           WHHHHHLLLLWWLLLLLLLWW
           WHHHHHLLLLWWLLLLLLLWW
           WWHHLLLLLLLWWLLLLLLLW
           WWHHLLLLLLLWWLLLLLLLW
           WWWWWWWWHWWWWLLLLLLLW
           WHHHHHLLLLWWLLLLLLLWW
           WHHHHHHHHHWWLLLLLLWWW
           WHHHHHDDDDDLLLLLLLWWW
           WHHHHHDDDDDLLLLLLLWWW
           WHHHHHDDDDDLLLLLLLWWW
           WHHHHHDDDDDWWLLLLLWWW
           WHHHHDDDDDDLLLLWWWWWW
           WWHHHHDDDDDDLWWWWWWWW
           WWHHHHDDDDDLLLWWWWWWW
           WHHHHHDDDDDLLLLLLLWWW
           WHHHHDDDDDDLLLLWWWWWW
           WWHHHHDDDDDLLLWWWWWWW
           WWWHHHHLLLLLLLWWWWWWW
           WWWHHHHHHWWWWWWWWWWWW
           WWWWWWWWWWWWWWWWWWWWW"""

island = Island(geogr)


scale_factor = .8
img_size = (16 * scale_factor,10 * scale_factor)
fig = plt.figure(figsize=img_size)

ax = fig.add_gridspec(12, 3)



map_ax = fig.add_subplot(ax[8:,1])
map_img = map_ax.imshow(island.bitmap)
map_ax.set_title('Map')
map_ax.axis('off')

herb_heat_ax = fig.add_subplot(ax[8:,0])
herb_heat_img = herb_heat_ax.imshow(island.bitmap,vmin=0,vmax=1)
plt.colorbar(herb_heat_img, ax=herb_heat_ax, location='left', pad=.05)
herb_heat_ax.set_title('Herbivores')
herb_heat_ax.axis('off')


carn_heat_ax = fig.add_subplot(ax[8:,2])
carn_heat_img = carn_heat_ax.imshow(island.bitmap, vmin=0,vmax=1)
plt.colorbar(carn_heat_img, ax=carn_heat_ax)
carn_heat_ax.set_title('Carnivores')
carn_heat_ax.axis('off')

map_title_ax = fig.add_axes([0, 0.12, .1, .25]) # llx, lly, w, h
map_title_ax.text(0.5, 0.5, 'Population\ndensity', horizontalalignment='center', verticalalignment='center', fontsize=15, rotation=45)
map_title_ax.axis('off')


pop_plot_llx = .05
pop_plot_lly = .3
pop_ax = fig.add_subplot(ax[0:3,:])
pop_plot = pop_ax.plot([0,1,2,3,4,5,6,7,8,9,10], [0,1,2,3,4,5,6,7,8,9,10])
pop_ax.set_title('Population')

pop_title_ax = fig.add_axes([0, .7, .1, .18]) # llx, lly, w, h
pop_title_ax.text(0.5, 0.5, 'Population\nHistory', horizontalalignment='center', verticalalignment='center', fontsize=15, rotation=45)
pop_title_ax.axis('off')

random.seed(0)
dist1 = [random.gauss(8,1) for _ in range(1000)]
dist2 = [random.gauss(6,.5) for _ in range(1000)]

hist1_ax = fig.add_subplot(ax[4:7,0])
hist1_ax.hist(dist1)
hist1_ax.set_title('Histogram')

hist1_title_ax = fig.add_axes([0, .44, .1, .18]) # llx, lly, w, h
hist1_title_ax.text(0.5, 0.5, 'Normalized\nhistograms', horizontalalignment='center', verticalalignment='center', fontsize=15, rotation=45)
hist1_title_ax.axis('off')


hist_ax2 = fig.add_subplot(ax[4:7,1])
hist_ax2.hist(dist2)
hist_ax2.set_title('Histogram')

hist_ax3 = fig.add_subplot(ax[4:7,2])
hist_ax3.hist(dist2)
hist_ax3.set_title('Histogram')

text_ax = fig.add_axes([.05, .9, .2, .06]) # llx, lly, w, h
year = 0
year_txt = f"Year: {year}"
year_counter = text_ax.text(0.5, 0.5, year_txt, horizontalalignment='center', verticalalignment='center', fontsize=20)
text_ax.axis('off')

#                   R    G    B
rgb_value = {'W': (0.13, 0.00, 1.00),  # blue
             'L': (0.00, 0.62, 0.00),  # dark green
             'H': (0.20, 1.00, 0.42),  # light green
             'D': (1.00, 1.00, 0.40)}  # light yellow



landscape_ax = fig.add_axes([.4, .01, .22, .09]) # llx, lly, w, h
landscape_ax.axis('off')

landscape_ax.add_patch(plt.Rectangle((0, .6), 0.2, 0.4, edgecolor='none',
                                  facecolor=rgb_value['W']))
landscape_ax.text(.22, 0.7, 'Water', transform=landscape_ax.transAxes)

landscape_ax.add_patch(plt.Rectangle((0, .0), 0.2, 0.4, edgecolor='none',
                                  facecolor=rgb_value['D']))
landscape_ax.text(.22, 0.16, 'Desert', transform=landscape_ax.transAxes)

landscape_ax.add_patch(plt.Rectangle((.5, .6), 0.2, 0.4, edgecolor='none',
                                  facecolor=rgb_value['L']))
landscape_ax.text(.73, .7, 'Lowland', transform=landscape_ax.transAxes)

landscape_ax.add_patch(plt.Rectangle((0.5, .0), 0.2, 0.4, edgecolor='none',
                                  facecolor=rgb_value['H']))
landscape_ax.text(.73, 0.16, 'Highland', transform=landscape_ax.transAxes)





plt.show()