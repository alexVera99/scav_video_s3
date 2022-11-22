"""Script to convert videos to the 4 Codecs: VP8, VP9, H265 and AV1."""
import pathlib
import logging

import converters as conv


def main():
    """
    Convert the given videos to the 4 video codecs.

    :return: no return
    """
    logging.basicConfig(level=logging.INFO)

    filenames = [pathlib.Path("../data/bbb_short_160_120.mp4"),
                 pathlib.Path("../data/bbb_short_360_240.mp4"),
                 pathlib.Path("../data/bbb_short_640_480.mp4"),
                 pathlib.Path("../data/bbb_short_1280_720.mp4")]

    for _f in filenames:
        filename_vp8 = conv.convert_video_to_vp8(_f)
        filename_vp9 = conv.convert_video_to_vp9(_f)
        filename_h265 = conv.convert_video_to_h265(_f)
        filename_av1 = conv.convert_video_to_av1(_f)

        print(filename_vp8)
        print(filename_vp9)
        print(filename_h265)
        print(filename_av1)


if __name__ == "__main__":
    main()
