import os
import imageio

current = ''
images_names = os.listdir()
images_names.sort()
images = []

for filename in images_names:
    if 'ep' not in filename:
        continue
    episode = filename.split('ep')[1].split('_')[0]
    if current == episode:
        images.append(imageio.imread(filename))
    elif current:
        imageio.mimsave(f'./gifs/{episode}.gif', images, duration=0.5)
        images = [imageio.imread(filename)]
        current = episode
    else:
        current = episode
        images = [imageio.imread(filename)]



