from biosim.island import Island
import matplotlib.pyplot as plt
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

img_size = (16/1.3,9/1.3)
fig = plt.figure(figsize=img_size)

map_lly = .65
map_spaceing = .35
map_start_llx = -.04

map_ax = fig.add_axes([map_start_llx,map_lly,.3,.3]) # llx, lly, w, h
map_img = map_ax.imshow(island.bitmap)
map_ax.set_title('Map')
map_ax.set_xticks([])
map_ax.set_yticks([])

herb_heat_ax = fig.add_axes([map_start_llx - .01,map_lly - map_spaceing,.3,.3]) # llx, lly, w, h
herb_heat_img = herb_heat_ax.imshow(island.bitmap,vmin=0,vmax=1)
plt.colorbar(herb_heat_img, ax=herb_heat_ax)
herb_heat_ax.set_title('Herbivores')
herb_heat_ax.set_xticks([])
herb_heat_ax.set_yticks([])

carn_heat_ax = fig.add_axes([map_start_llx - .01,map_lly - 2* map_spaceing,.3,.3]) # llx, lly, w, h
carn_heat_img = carn_heat_ax.imshow(island.bitmap)
plt.colorbar(carn_heat_img, ax=carn_heat_ax)
carn_heat_ax.set_title('Carnivores')
carn_heat_ax.set_xticks([])
carn_heat_ax.set_yticks([])

pop_plot_llx = .63
pop_ax = fig.add_axes([pop_plot_llx,map_lly,.35,.3]) # llx, lly, w, h
pop_plot = pop_ax.plot([0,1,2,3,4,5,6,7,8,9,10], [0,1,2,3,4,5,6,7,8,9,10])

plt.show()