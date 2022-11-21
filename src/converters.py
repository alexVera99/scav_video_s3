import pathlib
import logging

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
        output_filename = f"{video_name}_VP9"

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

    logging.info("Running the first pass")
    _, stderr = ut.exec_in_shell_wrapper(cmd_pass_1)
    ut.check_shell_stderr(stderr,
                          f"Could not convert the video {filename_path} "
                          f"to VP9 (First Pass)")
    logging.info("First pass finished")

    logging.info("Running the second pass")
    _, stderr = ut.exec_in_shell_wrapper(cmd_pass_2)
    ut.check_shell_stderr(stderr,
                          f"Could not convert the video {filename_path} "
                          f"to VP9 (Second Pass)")
    logging.info("Second pass finished")

    logging.info("Removing second ffmpeg log files")
    cmd_remove = ["rm", "-rf", "ffmpeg2pass-0.log"]

    stdout, stderr = ut.exec_in_shell_wrapper(cmd_remove)
    ut.check_shell_stderr(stderr,
                          f"Couldn't remove log files.")

    return output_filename_path


def convert_video_to_h265(filename_path: pathlib.Path,
                          output_filename: str = ""):
    """
    Convert the video to H265 codec. Inspired in \
    https://www.maketecheasier.com/encode-h265-video-using-ffmpeg/.

    :param filename_path: video filename path
    :param output_filename: output filename
    :return: created video filename
    """
    if output_filename == "":
        video_name = filename_path.name.split(".")[0]
        output_filename = f"{video_name}_H265"

    output_filename_path = ut.rename_from_path(filename_path,
                                               output_filename,
                                               "mp4")
    cmd = ["ffmpeg", "-y",
           "-i", filename_path,
           "-c:a", "copy",
           "-c:v", "libx265",
           output_filename_path]

    logging.info(f"Converting {filename_path} to H265")
    _, stderr = ut.exec_in_shell_wrapper(cmd)
    logging.info(f"{filename_path} converted to H265")

    ut.check_shell_stderr(stderr,
                          f"Could not convert the video {filename_path}"
                          "to H265.")

    return output_filename_path


def convert_video_to_av1(filename_path: pathlib.Path,
                          output_filename: str = ""):
    """
    Convert the video to AV1 codec using the libaom library. Inspired in \
    https://trac.ffmpeg.org/wiki/Encode/AV1#SVT-AV1.

    :param filename_path: video filename path
    :param output_filename: output filename
    :return: created video filename
    """
    if output_filename == "":
        video_name = filename_path.name.split(".")[0]
        output_filename = f"{video_name}_AV1"

    output_filename_path = ut.rename_from_path(filename_path,
                                               output_filename,
                                               "mkv")
    cmd = ["ffmpeg", "-y",
           "-i", filename_path,
           "-c:v", "libaom-av1",
           "-crf", "30",
           output_filename_path]

    logging.info(f"Converting {filename_path} to AV1")
    _, stderr = ut.exec_in_shell_wrapper(cmd)
    logging.info(f"{filename_path} converted to AV1")

    ut.check_shell_stderr(stderr,
                          f"Could not convert the video {filename_path}"
                          "to AV1.")

    return output_filename_path
