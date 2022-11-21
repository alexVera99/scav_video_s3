import pathlib

import PySimpleGUI as sg
from enum import Enum
import multiprocessing as mp

import exercise_1 as ex_1


class Codec(Enum):
    """Describe the possible video codecs in our module."""

    AV1 = "AV1"
    H265 = "H265"
    VP8 = "VP8"
    VP9 = "VP9"


class ConvertController:
    def __init__(self):
        self.convert_functions = {
            Codec.H265.value: ex_1.convert_video_to_h265,
            Codec.AV1.value: ex_1.convert_video_to_av1,
            Codec.VP8.value: ex_1.convert_video_to_vp8,
            Codec.VP9.value: ex_1.convert_video_to_vp9,
        }

    def convert(self, filename, codec: Codec):
        output_filename = self.convert_functions[codec](filename)
        print(output_filename)
        return output_filename


class ConvertView:
    def __init__(self, font, font_size):
        self.layout = [
            [sg.Text(text="Please, choose a codec", font=(font, font_size))],
            [sg.InputCombo([Codec.AV1.value,
                            Codec.H265.value,
                            Codec.VP8.value,
                            Codec.VP9.value],
                           size=(25, 1), key="-CODEC-",
                           default_value=Codec.H265.value)],
            [sg.Text("Search video", font=(font, font_size)),
             sg.In(size=(25, 1), enable_events=True, key="-FILENAME-"),
             sg.FileBrowse()],
            [sg.Button(button_text="Convert", key="-CONVERT-BUTTON-")]
        ]

        self.window = None

    def setup_view(self):
        self.window = sg.Window(title="Video codec converter",
                                layout=self.layout)

    def kill_window(self):
        self.window.close()


def main():
    convert_view = ConvertView("Helvetica", "11")

    convert_view.setup_view()

    convert_controller = ConvertController()

    while True:
        event, values = convert_view.window.read()
        print(event)
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        elif event == "-CONVERT-BUTTON-":
            codec = values["-CODEC-"]
            filename = pathlib.Path(values["-FILENAME-"])

            process = mp.Process(target=convert_controller.convert,
                                 args=(filename, codec,))
            process.start()


if __name__ == "__main__":
    main()
