"""Codec Video Converter Desktop app."""
import pathlib
from enum import Enum
import PySimpleGUI as sGui

import converters as conv


class Codec(Enum):
    """Describe the possible video codecs in our module."""

    AV1 = "AV1"
    H265 = "H265"
    VP8 = "VP8"
    VP9 = "VP9"


class ConvertModel:
    """Map the Codec to its conversion function."""

    def __init__(self):
        """Initialize ConvertModel."""
        self.convert_functions = {
            Codec.H265.value: conv.convert_video_to_h265,
            Codec.AV1.value: conv.convert_video_to_av1,
            Codec.VP8.value: conv.convert_video_to_vp8,
            Codec.VP9.value: conv.convert_video_to_vp9,
        }

    def convert(self, filename: pathlib.Path,
                codec: Codec):
        """
        Convert the given video to the specified video codec.

        :param filename: video filename. Type: pathlib.Path
        :param codec: codec to convert. Type: Codec.value
        :return: output filename
        """
        output_filename = self.convert_functions[codec](filename)
        return output_filename


class ConvertController:
    """Control actions from model and ui changes from viewer."""

    def __init__(self, viewer):
        """
        Control actions from model and ui changes viewer.

        :param viewer: UI implementation based on pysimplegui.
        """
        self.viewer = viewer
        self.model = ConvertModel()

    def read_events(self):
        """
        Get the events from the viewer window.

        :return:
        """
        return self.viewer.window.read()

    def convert(self, filename, codec):
        """
        Convert the given video to the specified codec and update viewer.

        :param filename: video filename
        :param codec: codec to convert to
        :return: no return
        """
        self.viewer.show_waiting_message()
        self.viewer.disable_buttons()

        try:
            output_filename = self.model.convert(filename,
                                                 codec)

            message = f"Done! The video has been created at \n" \
                      f"{output_filename}"
            self.viewer.show_success_message(message)

        except Exception:
            message = f"Could not convert the video \n{filename}"
            self.viewer.show_fail_message(message)

        self.viewer.enable_buttons()


class ConvertView:
    """Implement the UI using PySimpleGUI."""

    def __init__(self, font, font_size):
        """
        UI for Convert video.

        :param font: font to use in the UI
        :param font_size: size of the font to use in the UI
        """
        self.button_color = "gray"
        self.bg_color = "#3C3F41"
        self.title_bg_color = "gray"
        self.text_bg_color = self.bg_color

        col_layout = [
            [sGui.Titlebar(title="Codec converter",
                           font=(font, font_size),
                           background_color=self.title_bg_color,
                           icon="../media/icon_small.png")],
            [sGui.Text(text="Please, choose a codec",
                       font=(font, font_size),
                       background_color=self.bg_color),
             sGui.InputCombo([Codec.AV1.value,
                              Codec.H265.value,
                              Codec.VP8.value,
                              Codec.VP9.value],
                             size=(25, 1),
                             key="-CODEC-",
                             font=(font, font_size),
                             default_value=Codec.H265.value)],
            [sGui.Text("Search video",
                       font=(font, font_size),
                       background_color=self.bg_color),
             sGui.In(size=(25, 1),
                     enable_events=True,
                     key="-FILENAME-",
                     font=(font, font_size)),
             sGui.FileBrowse(button_color=self.button_color,
                             key="-FILE-BROWSER-BUTTON-",
                             font=(font, font_size))],
            [sGui.Button(button_text="Convert",
                         key="-CONVERT-BUTTON-",
                         font=(font, font_size),
                         button_color=self.button_color)],
            [sGui.Text(text="Done!",
                       font=(font, font_size),
                       text_color="green",
                       key="-SUCCESS-",
                       visible=False,
                       background_color=self.bg_color,
                       size=(40, 5))],
            [sGui.Text(text="Something went wrong",
                       font=(font, font_size),
                       text_color="red",
                       key="-ERROR-",
                       visible=False,
                       background_color=self.bg_color,
                       size=(40, 5))],
            [sGui.Text(text="Converting",
                       font=(font, font_size),
                       text_color="yellow",
                       key="-WAIT-",
                       visible=False,
                       background_color=self.bg_color)]
        ]

        self.layout = [
            [sGui.Column(col_layout,
                         element_justification='center',
                         expand_x=True,
                         background_color=self.bg_color)],
        ]

        self.window = None

    def setup_view(self):
        """
        Load the Window for this view.

        :return:no return
        """
        self.window = sGui.Window(title="Video codec converter",
                                  layout=self.layout,
                                  background_color=self.bg_color,)

    def kill_window(self):
        """
        Kill the window for this view.

        :return: no return
        """
        self.window.close()

    def show_success_message(self, message: str):
        """
        Show a success message.

        :param message: message to show.
        :return: no return
        """
        self.window["-ERROR-"].Update(visible=False)
        self.window["-WAIT-"].Update(visible=False)
        self.window["-SUCCESS-"].Update(message)
        self.window["-SUCCESS-"].Update(visible=True)

    def show_fail_message(self, message: str):
        """
        Show a fail message.

        :param message: fail message to show
        :return: no return
        """
        self.window["-SUCCESS-"].Update(visible=False)
        self.window["-WAIT-"].Update(visible=False)

        self.window["-ERROR-"].Update(visible=True)
        self.window["-ERROR-"].Update(message)

    def show_waiting_message(self, message: str = ""):
        """
        Show a waiting message.

        :param message: waiting message to show
        :return: no return
        """
        self.window["-ERROR-"].Update(visible=False)
        self.window["-SUCCESS-"].Update(visible=False)

        if message != "":
            self.window["-WAIT-"].Update(message)
        self.window["-WAIT-"].Update(visible=True)

    def disable_buttons(self):
        """
        Disable all the UI buttons.

        :return: no return
        """
        self.window["-FILE-BROWSER-BUTTON-"].Update(disabled=True)
        self.window["-CODEC-"].Update(disabled=True)
        self.window["-CONVERT-BUTTON-"].Update(disabled=True)

    def enable_buttons(self):
        """
        Enable all the UI buttons.

        :return: no return
        """
        self.window["-FILE-BROWSER-BUTTON-"].Update(disabled=False)
        self.window["-CODEC-"].Update(disabled=False)
        self.window["-CONVERT-BUTTON-"].Update(disabled=False)


def main():
    """
    Execute the main logic of the Desktop App.

    :return: no return
    """
    viewer = ConvertView("Helvetica", "18")
    viewer.setup_view()

    convert_controller = ConvertController(viewer)

    while True:
        event, values = convert_controller.read_events()

        if event == sGui.WIN_CLOSED:
            viewer.kill_window()
            break

        if event == "-CONVERT-BUTTON-":
            codec = values["-CODEC-"]
            filename = pathlib.Path(values["-FILENAME-"])

            viewer.window.perform_long_operation(lambda:
                                                 convert_controller.convert(
                                                     filename,
                                                     codec),
                                                 '-CONVERTED-')


if __name__ == "__main__":
    main()
