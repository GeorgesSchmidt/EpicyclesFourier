import imageio

reader = imageio.get_reader('Anim-epicycles.mp4')
fps = reader.get_meta_data()['fps']

writer = imageio.get_writer('animation_readme.gif', fps=fps)
for frame in reader:
    writer.append_data(frame)
writer.close()