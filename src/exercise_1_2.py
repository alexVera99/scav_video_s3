"""Create a mosaic with 4 videos."""
import glob
import pathlib
import logging

import utils as ut


def create_mosaic_4_videos(filename_1: pathlib.Path,
                           filename_2: pathlib.Path,
                           filename_3: pathlib.Path,
                           filename_4: pathlib.Path,
                           output_filename: pathlib.Path):
    """
    Create a mosaic of 4 videos. Inspired by \
    https://stackoverflow.com/questions/36268431/video-grid-with-vstack-and-hstack.

    :param filename_1: video filename of any codec
    :param filename_2: video filename of any codec
    :param filename_3: video filename of any codec
    :param filename_4: video filename of any codec
    :param output_filename: output filename
    :return: no return
    """
    cmd = ["ffmpeg", "-y",
           "-i", filename_1,
           "-i", filename_2,
           "-i", filename_3,
           "-i", filename_4,
           "-filter_complex",
           "[0:v][1:v]hstack[t];[2:v][3:v]hstack[b];[t][b]vstack[v]",
           "-map", "[v]",
           "-map", "0:a",
           output_filename]

    logging.info("Starting to build the mosaic")

    _, stderr = ut.exec_in_shell_wrapper(cmd)

    logging.info("The mosaic has been created at \n%s", output_filename)

    ut.check_shell_stderr(stderr,
                          "Could not obtain the mosaic")


def main():
    """
    Create a mosaic of 4 videos of different codecs for all the \
    following resolutions: 160x120, 360x240, 480p and 720p.

    :return: no return.
    """
    logging.basicConfig(level=logging.INFO)

    patterns_reso = {"160x120": "../data/*_160_120_*.*",
                     "360x240": "../data/*_360_240_*.*",
                     "480p": "../data/*_640_480_*.*",
                     "720p": "../data/*_1280_720_*.*"}

    for _n, _p_r in patterns_reso.items():
        filenames = glob.glob(_p_r)
        filenames.sort()
        f_1, f_2, f_3, f_4 = [pathlib.Path(f) for f in filenames]

        output_filename = f_1.parent / f"mosaic_{_n}.mp4"
        create_mosaic_4_videos(f_1, f_2, f_3, f_4, output_filename)


if __name__ == "__main__":
    main()
