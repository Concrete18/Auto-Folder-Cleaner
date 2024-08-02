import shutil, json
from pathlib import Path

class Config:


    def __init__(self, config=None) -> None:
        if config:
            self.config = Path(config)
        else:
            default_config_name = "config.json"
            self.config = Path(default_config_name)
            if not self.config.exists():
                template = Path("template_config.json")
                shutil.copyfile(template, default_config_name)

    def setup(self):
        """
        Initializes settings from config.
        """
        with open(self.config) as json_file:
            data = json.load(json_file)
        # setting setup
        self.settings = data["settings"]

        # default watcher folder
        self.watched_folder = self.settings["watched_folder"]

        # Enables asking to delete files that match a filename from delete_def.
        self.ask_to_delete = self.settings["ask_to_delete"]

        # Toggles renaming
        self.rename = self.settings["rename"]

        # Enables progress bar.
        self.progress_bar = self.settings["progress_bar"]

        # True sets progress bar to use ascii in case of unicode issues.
        self.ascii = self.settings["ascii_bar"]

        # Sets file types into groups.
        self.file_type_groups = data["file_type_groups"]

        # Sets destination based on file group.
        self.file_group_dest = data["file_group_dest"]

        # Checks for keywords in file names.
        self.keywords_dest = data["keywords_dest"]

        # Lists special cases for file type destinations.
        self.special_case_dest = data["special_case_dest"]

        # Lists files to possible delete instead of moving.
        self.delete_def = data["delete_def"]

        # loads the rename presets
        self.file_rename_presets = data["file_rename"]

if __name__ == "__main__":
    config = Config()
    config.setup()

    print(dir(config))
