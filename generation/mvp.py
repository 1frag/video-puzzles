import ffmpeg_utils


def to_gif(i):
    ffmpeg_utils.to_gif(
        input_file=f'../www/data/1/mp4/out-{i}.mp4',
        output_file=f'../www/data/1/gif/out-{i}.gif',
    )


def crop(w, h, x, y, i):
    ffmpeg_utils.crop(
        width=w,
        height=h,
        left=x,
        top=y,
        input_file='../1.mp4',
        output_file=f'../www/data/1/mp4/out-{i}.mp4',
    )


def main(parts_x, parts_y):
    i = 1

    width = 1280
    height = 720

    w = width // parts_x
    h = height // parts_y

    for x in range(0, width, w):
        for y in range(0, height, h):
            crop(w, h, x, y, i)
            i += 1

    for i in range(1, i):
        to_gif(i)
