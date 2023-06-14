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



ini_herbs = [{'loc': (2,2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(800)]}]

ini_carn = [{'loc': (2, 2),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(400)]}]

island = Island(geogr)
island.add_population(ini_herbs)
island.add_population(ini_carn)

map_rgb = [[(0,0,0) for _ in range(island.map_width)] for _ in range(island.map_height)]


habital_map = island.habital_map



img_size = (16/1.3,9/1.3)
fig = plt.figure(figsize=img_size)

map_lly = 0.05
map_spaceing = .17
map_start_llx = -.04

map_ax = fig.add_axes([map_start_llx,map_lly,.3,.3]) # llx, lly, w, h
map_img = map_ax.imshow(island.bitmap)
map_ax.set_title('Map')
map_ax.set_xticks([])
map_ax.set_yticks([])

herb_heat_ax = fig.add_axes([map_start_llx + map_spaceing,map_lly,.3,.3]) # llx, lly, w, h
herb_heat_img = herb_heat_ax.imshow(island.bitmap,vmin=0,vmax=1)
plt.colorbar(herb_heat_img, ax=herb_heat_ax)
herb_heat_ax.set_title('Herbivores')
herb_heat_ax.set_xticks([])
herb_heat_ax.set_yticks([])

carn_heat_ax = fig.add_axes([map_start_llx + 2* map_spaceing,map_lly,.3,.3]) # llx, lly, w, h
carn_heat_img = carn_heat_ax.imshow(island.bitmap)
carn_heat_ax.set_title('Carnivores')
carn_heat_ax.set_xticks([])
carn_heat_ax.set_yticks([])

pop_plot_llx = .63
pop_ax = fig.add_axes([pop_plot_llx,map_lly,.35,.3]) # llx, lly, w, h
pop_plot = pop_ax.plot([0,1,2,3,4,5,6,7,8,9,10], [0,1,2,3,4,5,6,7,8,9,10])



for year in range(1, SIM_YEARS + 1):
    for loc, cell in island.habital_map.items():
        map_rgb[loc[0] - 1][loc[1] - 1] = (0, 0, 0)
        if len(cell.herbivore) > 0:
            map_rgb[loc[0]-1][loc[1]-1] = (0,0, 255)
        if len(cell.carnivore) > 0:
            map_rgb[loc[0]-1][loc[1]-1] = (255, 0, 0)

    island.migrate_animals()
    #img_ax.set_data(map_rgb)
    #plt.pause(0.0001)

plt.show()



