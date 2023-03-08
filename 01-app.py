from textual.app import App, ComposeResult
from textual_filedrop import FileDrop


class EOSUploadApp(App):
    DEFAULT_CSS = """
        Screen {
            align: center middle;
        }
    """

    BINDINGS = [("q", "exit", "Quit"), ("d", "toggle_dark", "Toggle dark mode")]

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_exit(self) -> None:
        """An action to exit."""
        self.exit()

    def compose(self) -> ComposeResult:
        yield FileDrop(id="filedrop")

    def on_mount(self):
        self.query_one("#filedrop").focus()

    def on_file_drop_dropped(self, event: FileDrop.Dropped) -> None:
        path = event.path
        filepaths = event.filepaths
        filenames = event.filenames
        filesobj = event.filesobj
        print(path, filepaths, filenames, filesobj)


if __name__ == "__main__":
    app = EOSUploadApp()
    app.run()
