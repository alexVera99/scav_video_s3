import pathlib

import utils as ut


def convert_video_to_vp8(filename_path: pathlib.Path,
                         output_filename: str = ""):
    """
    Convert the video to VP8 codec.

    :param filename_path: video filename path
    :param output_filename: output filename
    :return: created video filename
    """

    if output_filename == "":
        video_name = filename_path.name.split(".")[0]
        output_filename = f"{video_name}_VP8"

    output_filename_path = ut.rename_from_path(filename_path,
                                               output_filename,
                                               "webm")

    cmd = ["ffmpeg", "-y",
           "-i", filename_path,
           "-c:v", "libvpx",
           "-crf", "10",
           "-b:v", "1M",
           "-c:a", "libvorbis",
           output_filename_path]

    _, stderr = ut.exec_in_shell_wrapper(cmd)

    ut.check_shell_stderr(stderr,
                          f"Could not convert the video {filename_path}")

    return output_filename_path


def convert_video_to_vp9(filename_path: pathlib.Path,
                         output_filename: str = ""):
    """
    Convert the video to VP9 codec. Inspired in \
    https://trac.ffmpeg.org/wiki/Encode/VP8.

    :param filename_path: video filename path
    :param output_filename: output filename
    :return: created video filename
    """
    if output_filename == "":
        video_name = filename_path.name.split(".")[0]
        output_filename = f"{video_name}_VP8"

    output_filename_path = ut.rename_from_path(filename_path,
                                               output_filename,
                                               "webm")

    cmd_pass_1 = ["ffmpeg", "-y",
                  "-i", filename_path,
                  "-c:v", "libvpx-vp9",
                  "-b:v", "1M",
                  "-pass", "1",
                  "-an",
                  "-f", "null", "/dev/null"]

    cmd_pass_2 = ["ffmpeg", "-y",
                  "-i", filename_path,
                  "-c:v", "libvpx-vp9",
                  "-b:v", "1M",
                  "-pass", "2",
                  "-c:a", "libopus",
                  output_filename_path]

    _, stderr = ut.exec_in_shell_wrapper(cmd_pass_1)
    ut.check_shell_stderr(stderr,
                          f"Could not convert the video {filename_path} "
                          f"(First Pass)")

    _, stderr = ut.exec_in_shell_wrapper(cmd_pass_2)
    ut.check_shell_stderr(stderr,
                          f"Could not convert the video {filename_path} "
                          f"(Second Pass)")

    return output_filename_path


def main():
    """
    Testing the above functions.

    :return: no return
    """
    filename = pathlib.Path("../data/bbb.mp4")

    #filename_vp8 = convert_video_to_vp8(filename)

    #print(filename_vp8)

    filename_vp9 = convert_video_to_vp9(filename)
    print(filename_vp9)

if __name__ == "__main__":
    main()
