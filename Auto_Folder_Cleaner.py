import winsound, shutil, math, json, os, re
from tqdm import tqdm
from pathlib import Path


class Cleaner:

    print(title := "Auto Folder Cleaner")

    def __init__(self, config=None) -> None:
        if config:
            self.config = Path(config)
        else:
            default_config_name = "config.json"
            self.config = Path(default_config_name)
            if not self.config.exists():
                template = Path("template_config.json")
                shutil.copyfile(template, default_config_name)

    def get_settings(self):
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

    def destination_check(self):
        """
        Checks all the destinations in the config file to be sure that all but
        the last folder in each destination exists. If the last folder is
        all that is missing, it will be created during the move process.
        """
        print(f"\nMaking sure file destinations are valid.")
        missing_dests = []
        dir_list = [
            self.file_group_dest,
            self.special_case_dest,
            self.keywords_dest,
        ]
        for dirs in dir_list:
            for dest in dirs.values():
                if dest == "skip":
                    continue
                if type(dest) == list:
                    dest = dest[1]
                directory = os.path.dirname(dest)
                if not os.path.exists(directory):
                    if dest not in missing_dests:
                        print(dest)
                        missing_dests.append(dest)
        return missing_dests

    @staticmethod
    def get_file_type(file_name):
        """
        Gets file type from the given file name. It only uses the last period separating extension.
        """
        file_type = ""
        split_string = file_name.split(".")
        file_type = f".{split_string[-1]}"
        return file_type

    def set_destination(self, file_name):
        """
        This function looks for matches in file extensions and keywords.
        It sets the destination for the file or sets it to skip if the file was deleted.

        Keyword arguments:

        file -- file that is being checked for file extension and keyword matches
        """
        file_type = self.get_file_type(file_name)
        destination = "skip"
        # for loop that checks for file group matches
        for file_group, file_type_list in self.file_type_groups.items():
            if file_type in file_type_list:
                # sets destination based on file group
                destination = self.file_group_dest[file_group]
                if file_type in self.special_case_dest:
                    # sets destination based on special case
                    destination = self.special_case_dest[file_type]
                # for loop that checks for keyword matches
                for (keyword, keyword_data) in self.keywords_dest.items():
                    # checks for match with upper case removed
                    if keyword.lower() in file_name.lower():
                        if file_type in keyword_data[0]:
                            destination = keyword_data[1]
                        elif file_group == keyword_data[0][0]:
                            destination = keyword_data[1]
        # checks if file was moved previously and cancels move
        if destination == "skip" or os.path.exists(
            os.path.join(destination, file_name)
        ):
            return
        # end destination for file entered as file argument
        return destination

    @staticmethod
    def convert_size(bytes):
        """
        Converts size given in `bytes` to best fitting unit of measure.
        """
        size_name = ("B", "KB", "MB", "GB", "TB")
        try:
            i = int(math.floor(math.log(bytes, 1024)))
            p = math.pow(1024, i)
            s = round(bytes / p, 2)
            return f"{s} {size_name[i]}"
        except ValueError:
            return "0 bits"

    def setup_queue(self):
        """
        Sets up queue of files to be moved later.
        """
        print(f"\nChecking for new files in {self.watched_folder}")
        watched_files = os.scandir(self.watched_folder)
        self.move_queue = []
        self.queue_length = 0
        self.queue_size = 0
        large_files = 0
        for file in watched_files:
            file_type = self.get_file_type(file.name)
            if file_type in self.delete_def and self.ask_to_delete:
                response = input(f"\nDo you want to delete {file.name}?\n")
                if response.lower() in ["yes", "y", "yeah"]:
                    os.remove(file.path)
                    continue
            if not file.name.startswith(".") and file.is_file():
                destination = self.set_destination(file.name)
                if destination != None:
                    file_size = os.path.getsize(file.path)
                    dict = {
                        "file_name": file.name,
                        "file_size": file_size,
                        "target": file.path,
                        "destination": destination,
                    }
                    if file_size > 1e9:
                        large_files += 1
                    self.move_queue.append(dict)
                    self.queue_length += 1
                    self.queue_size += file_size
        self.move_queue = sorted(self.move_queue, key=lambda i: i["file_size"])
        if len(self.move_queue) == 0:
            print(f"> No new files found.")
            self.delete_empty_folders(self.watched_folder)
            input("\nPress Enter to close\n")
            exit()
        elif self.queue_length == 1:
            is_files = "file"
        else:
            is_files = "files"
        converted_size = self.convert_size(self.queue_size)
        print(
            f"> {self.queue_length} new {is_files} found totaling to {converted_size}."
        )
        if large_files > 0:
            print(
                f"> {large_files} large files need to transfer so give it time to prevent corruption."
            )
        return self.move_queue

    def file_rename(self, destination, target):
        """
        Runs through file_rename_presets and replaces the set strings with the new strings and then returns it.
        """
        file_name = os.path.basename(target)
        for string, replacement in self.file_rename_presets.items():
            pattern = re.compile(re.escape(string), re.IGNORECASE)
            file_name = pattern.sub(replacement, file_name)
            new_path = os.path.join(destination, file_name)
            if os.path.exists(new_path) or file_name[0] == ".":
                return os.path.join(destination, target)
        return new_path

    def file_move(self, target, destination):
        """
        Moves Target file to Destination after making the destination directory if it does not exist.
        It will also leave the file where it is if it already exists at the destination.

        Keyword arguments:

        target -- file to move

        destination -- destination of target file
        """
        if os.path.isdir(destination) is False:  # checks if destination directory exist
            os.mkdir(destination)  # makes directory if it does not exist
        if self.rename:
            destination = self.file_rename(destination, target)
        shutil.move(target, destination)

    def move_file_queue(self):
        """
        Goes through the list of dictionarys in the move_queue to send all files to their correct destinations.
        It will employ a progress bar if enabled in the config.
        """
        try:
            if self.progress_bar:
                # uses progress bar
                # TODO set to use tqdm.concurrent
                with tqdm(
                    total=self.queue_size,
                    ascii=self.ascii,
                    unit="byte",
                    unit_scale=1,
                    dynamic_ncols=1,
                ) as bar:
                    bar.set_description(desc=f"> Moving Files", refresh=1)
                    for entry in self.move_queue:
                        self.file_move(entry["target"], entry["destination"])
                        bar.update(entry["file_size"])
                    bar.close()
            else:
                # does not use progress bar
                for entry in self.move_queue:
                    self.file_move(entry["target"], entry["destination"])
            print("> All files have been moved")
        except KeyboardInterrupt:
            # TODO delete partial copy if in progress
            path = os.path.join(entry["destination"], os.path.basename(entry["target"]))
            print(path)
            if os.path.exists(path):
                print("Removed partial copy.")
                # os.remove(path)
            print("Cancelled folder clean")
            return
        except ModuleNotFoundError:
            print(
                "Please disable progress bar in config or install the module via Pip."
            )

    @staticmethod
    def delete_empty_folders(directory):
        """
        Deletes empty folders in the watched_folder entered as an argument.
        """
        delete_total = 0  # init var for total empty folders deleted
        print(f"\nChecking for empty directories.")
        for file in os.scandir(directory):
            # checks if file is a folder instead of a file
            folder_exists = os.path.exists(file.path)
            is_folder = not os.path.isfile(file.path)
            if folder_exists and is_folder:
                # detects if folder is empty
                if len(os.listdir(file.path)) == 0:
                    try:
                        os.rmdir(file.path)
                    # error check in case of unseen circumstance
                    except OSError:
                        print(f"Failed to delete {file.name}\nIt is not empty.")
                    delete_total += 1
        # prints info if empty folders were deleted
        if delete_total == 1:
            print(f"> Deleted 1 empty folder.")
        elif delete_total > 1:
            print(f"> Deleted {delete_total} empty folders.")
        else:
            print(f"> No empty folders were found.")

    def completion_sound(self):
        """
        Plays a completion sound.
        """
        winsound.PlaySound("Exclamation", winsound.SND_ALIAS)

    def run(self):
        """
        Runs main script process.
        """
        self.get_settings()
        # checks for missing destinations
        missing_dests = self.destination_check()
        if len(missing_dests) > 0:
            print("> The below base directories are missing.\n")
            print(missing_dests)
            if input("\nDo you want to continue?").lower() in ["no", "n"]:
                exit()
        else:
            print("> All destinations are valid.")
        # sets up a queue for what needs to be moved
        self.setup_queue()
        print("\nStarting Folder Clean | Use Ctrl C if you need to cancel")
        self.move_file_queue()
        if self.settings["delete_empty_folders"]:
            self.delete_empty_folders(self.watched_folder)
        print("\nFolder Clean Complete")
        winsound.PlaySound("Exclamation", winsound.SND_ALIAS)
        if len(self.move_queue) > 5:
            response = input(
                "\nDo you want to see the file Manifist?\nIf not press enter to close.\n"
            )
            if response.lower() not in ["yes", "y", "yeah"]:
                exit()
        print("\nFile Manifest")
        for entry in self.move_queue:
            print(f'\n> Name: {entry["file_name"]}\n  Dest: {entry["destination"]}')
        # TODO allow opening folders that files where moved to after prompt
        input("\nPress enter to close.")


if __name__ == "__main__":
    Cleaner().run()
