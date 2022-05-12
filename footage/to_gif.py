import os
import imageio

search_dir = "./"
os.chdir(search_dir)
files = filter(os.path.isfile, os.listdir(search_dir))
files = [os.path.join(search_dir, f) for f in files if 'ep' in f]
files.sort(key=lambda x: os.path.getmtime(x))

images = []
gifs = {}

for filename in files:
    episode = filename.split('ep')[1].split('_')[0]
    if episode in gifs:
        gifs[episode].append(imageio.imread(filename))
    else:
        gifs[episode] = [imageio.imread(filename)]

[imageio.mimsave(f'./gifs/{i}.gif', gifs[i], duration=0.5) for i in gifs]



