# Auto Folder Cleaner

This script searches a watched directory in order to move files based on their filetypes and keywords.
It works by using for loops to go through files in the watched directory.
It checks for matches in a file type and keyword Dictionaries.

## Features

* Fully Configurable preferences. (_Example Below_)
* Auto move files based on keywords or filetypes.
* Keywords can be set to only work with a specific file group/s or a file type/s.
* Warning in case of config set destinations do not exist.
(only checks for directory 1 layer back - C:/Downloads/Audio Files -> C:/Downloads)
* Ask to delete files based on a delete file type list.
* Auto delete empty folders if config is set to 1.
* Threading for completing multiple transfers at a time.
* Unit Testing for verifying a few functions.

## Future Plans

* Add Recycle bin support (Windows).

## Preferences Example

Never use \ for paths, instead use \\ or / instead.

```json
{
    "settings":
        {
            "watched_folder": "C:/Downloads",
            "ask_to_delete": 1,
            "delete_empty_folders": 1,
            "progress_bar": 1
        },
    "dictionaries":
        {
            "file_type_groups":
                {
                    "audio": [".mp3", ".wav", ".flac"],
                    "image": [".jpg", ".png", ".gif", "tiff", "tif"],
                    "video": [".mp4", ".wave", ".mkv", ".mpeg", "mpeg4", ".avi", ".mpeg4", ".avi", ".wmv"],
                    "text": [".txt", ".doc", ".docx", ".pdf", ".odt"],
                    "spreadsheet": [".xls", ".xlsx", ".xlsm", ".ods"],
                    "compressed": [".deb", ".pkg", ".rar", ".rpm", ".tar", ".gz", ".z", ".zip"],
                    "executable": [".exe", ".bat", ".apk", ".bin", ".com", ".jar", ".msi", ".wsf"],
                    "presentation": [".key", ".odp", ".pps", ".ppt", ".pptx"],
                    "programming": [".c", ".class", ".cpp", ".cs", ".h", ".java", ".php", ".py", ".sh", ".swift", ".vb"]
                },
            "file_group_dest":
                {
                    "audio":"C:/Downloads/Audio Files",
                    "image":"C:/Downloads/Images",
                    "video":"C:/Downloads/Videos",
                    "text":"C:/Downloads/Documents",
                    "spreadsheet":"C:/Downloads/Spreadsheets",
                    "compressed":"C:/Downloads/Compressed Files",
                    "executable":"C:/Downloads/Executable",
                    "presentation":"C:/Downloads/Presentations",
                    "programming":"C:/Downloads/Programming"
                },
            "keywords_dest":
                {
                    "wallpaper": [[".jpg", ".png"], "C:/Downloads/Wallpapers"],
                    "Family": [[".jpg", ".png"], "C:/Downloads/Family Videos"],
                    "python": [[".py"], "C:/Downloads/Coding/Python"]
                },
            "special_case_dest":
                {
                    ".mkv":"C:/Downloads/HD Videos"
                },
            "delete_def":
                [
                    ".exe", ".test", ".zip", ".rar", ".7z"
                ]
        }
}
```
