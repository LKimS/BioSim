from biosim.island import Island
import matplotlib.pyplot as plt
import random
SIM_YEARS = 3

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

img_size = (16/1.3,10/1.3)
fig = plt.figure(figsize=img_size)

map_lly = .55
map_spacing = .25
map_start_llx = 0

map_size = .4

map_ax = fig.add_axes([.29,map_lly,map_size,map_size]) # llx, lly, w, h
map_img = map_ax.imshow(island.bitmap)
map_ax.set_title('Map')
map_ax.set_xticks([])
map_ax.set_yticks([])

herb_heat_ax = fig.add_axes([map_start_llx ,map_lly,map_size,map_size]) # llx, lly, w, h
herb_heat_img = herb_heat_ax.imshow(island.bitmap,vmin=0,vmax=1)
plt.colorbar(herb_heat_img, ax=herb_heat_ax, location='left', pad=0.05)
herb_heat_ax.set_title('Herbivores')
herb_heat_ax.set_xticks([])
herb_heat_ax.set_yticks([])

carn_heat_ax = fig.add_axes([map_start_llx + 2 * map_spacing + .08,map_lly,map_size,map_size]) # llx, lly, w, h
carn_heat_img = carn_heat_ax.imshow(island.bitmap)
plt.colorbar(carn_heat_img, ax=carn_heat_ax)
carn_heat_ax.set_title('Carnivores')
carn_heat_ax.set_xticks([])
carn_heat_ax.set_yticks([])

pop_plot_llx = .05
pop_plot_lly = .3
pop_ax = fig.add_axes([pop_plot_llx,pop_plot_lly,.9,.2]) # llx, lly, w, h
pop_plot = pop_ax.plot([0,1,2,3,4,5,6,7,8,9,10], [0,1,2,3,4,5,6,7,8,9,10])
pop_ax.set_title('Population')

random.seed(0)
dist1 = [random.gauss(8,1) for _ in range(1000)]
dist2 = [random.gauss(6,.5) for _ in range(1000)]

hist_lly = .05
hist_llx = .05
hist1_ax = fig.add_axes([hist_llx,hist_lly,.4,.18]) # llx, lly, w, h
hist1_ax.hist(dist1)
hist1_ax.set_title('Histogram')

hist_lly = .05
hist_llx = .05
hist_ax2 = fig.add_axes([hist_llx + .5,hist_lly,.4,.18]) # llx, lly, w, h
hist_ax2.hist(dist2)
hist_ax2.set_title('Histogram')


plt.show()