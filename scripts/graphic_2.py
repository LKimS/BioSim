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



img_size = (10,10)
fig = plt.figure(figsize=img_size)

ax = fig.add_gridspec(3, 3)



map_ax = fig.add_subplot(ax[0,1])
map_img = map_ax.imshow(island.bitmap)
map_ax.set_title('Map')
map_ax.axis('off')

herb_heat_ax = fig.add_subplot(ax[0,0])
herb_heat_img = herb_heat_ax.imshow(island.bitmap,vmin=0,vmax=1)
plt.colorbar(herb_heat_img, ax=herb_heat_ax, location='left', pad=.05)
herb_heat_ax.set_title('Herbivores')
herb_heat_ax.axis('off')


carn_heat_ax = fig.add_subplot(ax[0,2])
carn_heat_img = carn_heat_ax.imshow(island.bitmap, vmin=0,vmax=1)
plt.colorbar(carn_heat_img, ax=carn_heat_ax)
carn_heat_ax.set_title('Carnivores')
carn_heat_ax.axis('off')


pop_plot_llx = .05
pop_plot_lly = .3
pop_ax = fig.add_subplot(ax[1,:])
pop_plot = pop_ax.plot([0,1,2,3,4,5,6,7,8,9,10], [0,1,2,3,4,5,6,7,8,9,10])
pop_ax.set_title('Population')

random.seed(0)
dist1 = [random.gauss(8,1) for _ in range(1000)]
dist2 = [random.gauss(6,.5) for _ in range(1000)]

hist1_ax = fig.add_subplot(ax[2,0:2])
hist1_ax.hist(dist1)
hist1_ax.set_title('Histogram')


hist_ax2 = fig.add_subplot(ax[2,2])
hist_ax2.hist(dist2)
hist_ax2.set_title('Histogram')

text_ax = fig.add_axes([.05, .93, .2, .06]) # llx, lly, w, h
year = 0
year_txt = f"Year: {year}"
year_counter = text_ax.text(0.5, 0.5, year_txt, horizontalalignment='center', verticalalignment='center')
text_ax.axis('off')

#                   R    G    B
rgb_value = {'W': (0.13, 0.00, 1.00),  # blue
             'L': (0.00, 0.62, 0.00),  # dark green
             'H': (0.20, 1.00, 0.42),  # light green
             'D': (1.00, 1.00, 0.40)}  # light yellow



landscape_ax = fig.add_axes([.4, .9, .22, .8]) # llx, lly, w, h
landscape_ax.axis('off')

landscape_ax.add_patch(plt.Rectangle((0, .06), 0.11, 0.04, edgecolor='none',
                                  facecolor=rgb_value['W']))
landscape_ax.text(.12, 0.07, 'Water', transform=landscape_ax.transAxes)

landscape_ax.add_patch(plt.Rectangle((0, .01), 0.11, 0.04, edgecolor='none',
                                  facecolor=rgb_value['D']))
landscape_ax.text(.12, 0.02, 'Desert', transform=landscape_ax.transAxes)

landscape_ax.add_patch(plt.Rectangle((0.6, .06), 0.11, 0.04, edgecolor='none',
                                  facecolor=rgb_value['L']))
landscape_ax.text(.72, 0.07, 'Lowland', transform=landscape_ax.transAxes)

landscape_ax.add_patch(plt.Rectangle((0.6, .01), 0.11, 0.04, edgecolor='none',
                                  facecolor=rgb_value['H']))
landscape_ax.text(.72, 0.02, 'Highland', transform=landscape_ax.transAxes)





plt.show()