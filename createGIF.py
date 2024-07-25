import imageio

reader = imageio.get_reader('Anim_FFT_1.mp4')
fps = reader.get_meta_data()['fps']

writer = imageio.get_writer('animation_readme_fft.gif', fps=fps)
for frame in reader:
    writer.append_data(frame)
writer.close()