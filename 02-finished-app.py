from textual.app import App, ComposeResult
from textual_filedrop import FileDrop

import sys
import itkdb
client = itkdb.Client(use_eos=True)
from pathlib import Path

class EOSUploadApp(App):
    component = None

    DEFAULT_CSS = """
        Screen {
            align: center middle;
        }
    """

    def __init__(self, component):
        self.component = component
        super().__init__()

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

        response = self.upload_file(filenames[0], filepaths[0])
        if response:
            self.query_one("#filedrop").styles.border = ("round", "green")
            self.query_one("#filedrop").txt = f"Uploaded '[yellow]{filenames[0]}[/yellow]' to [yellow]{self.component}[/yellow]\n\nURL: {response['url']}\n\nComponent: https://itkpd-test.unicorncollege.cz/componentView?code={self.component}"
        else:
            self.query_one("#filedrop").styles.border = ("round", "red")
            self.query_one("#filedrop").txt = f"Failed to upload"


    def upload_file(self, filename, filepath):
        data = {
            "component": self.component,
            "title": filename,
            "description": "This is a test attachment descriptor",
            "type": "file",
            "url": Path(filepath),
        }

        try:
            with Path(filepath).open("rb") as fpointer:
                files = {"data": itkdb.utils.get_file_components({"data": fpointer})}
                response = client.post("createComponentAttachment", data=data, files=files)
        except itkdb.exceptions.ResponseException:
            return False

        return response


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('usage: python app.py 20UXXYYnnnnnnn')
        sys.exit(1)

    app = EOSUploadApp(sys.argv[1])
    app.run()
