import os


def to_gif(input_file: str, output_file: str):
    os.popen(
        f'ffmpeg -i {input_file} -vf "fps=10,scale=320:-1:flags=lanczos" '
        f'-c:v pam -f image2pipe - | convert -delay 10 - '
        f'-loop 0 -layers optimize {output_file}'
    ).read()


def crop(
        width: int,
        height: int,
        left: int,
        top: int,
        input_file: str,
        output_file: str,
):
    os.popen(f'ffmpeg -i {input_file} -y -filter:v "crop={width}:{height}:{left}:{top}" {output_file}').read()


def apply_mask(video_file: str, mask_file: str, output_file: str):
    os.popen(
        f'ffmpeg -y -i {video_file}  -i {mask_file} -filter_complex "[1:v]alphaextract[alf];[0:v][alf]alphamerge" '
        f'-c:v vp9 -an {output_file}'
    ).read()
