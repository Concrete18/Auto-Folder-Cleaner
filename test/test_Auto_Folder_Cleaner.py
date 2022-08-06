from Auto_Folder_Cleaner import Cleaner
import unittest, os, shutil


class TestDestinationCheck(unittest.TestCase):
    def setUp(self):
        self.App = Cleaner(config="template_config.json")
        self.App.get_settings()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.App.watched_folder = f"{script_dir}/test folder"

    def test_base_use(self):
        """
        ph
        """
        dir = self.App.watched_folder
        self.App.file_group_dest = {
            "audio": f"{dir}/Documents/Audio Files",
            "video": f"{dir}/Documents/Media/Videos",
        }
        self.App.special_case_dest = {
            ".mkv": f"{dir}/Documents/HD Videos",
        }
        self.App.keywords_dest = {
            "wallpaper": [[".jpg", ".png"], f"{dir}/Documents/Wallpapers"],
        }

        result = self.App.destination_check()
        answer = [
            "d:\\Google Drive\\Coding\\Python\\Scripts\\1-Complete-Projects\\Auto-Folder-Cleaner\\test/test folder/Documents/Media/Videos"
        ]
        self.assertEqual(result, answer)


class FileRename(unittest.TestCase):
    def setUp(self):
        self.App = Cleaner(config="template_config.json")
        self.App.file_rename_presets = {
            "deletethis": "",
            "this is a test": "Test Complete",
        }

    def test_base_use(self):
        """
        Tests for normal use.
        """
        result = self.App.file_rename("C:/", "this is a test.png")
        self.assertEqual(result, "C:/Test Complete.png")

        result = self.App.file_rename("C:/", "tHis iS a tEst.png")
        self.assertEqual(result, "C:/Test Complete.png")

    def test_same(self):
        """
        Tests for keeping file names the same if they would delete everything
        before the file type.
        """
        result = self.App.file_rename("C:/", "deletethis.png")
        self.assertEqual(result, "C:/deletethis.png")

        result = self.App.file_rename("C:/", "DeLEtEthIs.png")
        self.assertEqual(result, "C:/DeLEtEthIs.png")


class GetFileType(unittest.TestCase):
    def setUp(self):
        self.App = Cleaner(config="template_config.json")

    def test_single_file_type(self):
        """
        ph
        """
        self.assertEqual(self.App.get_file_type("wallpaper.png"), ".png")

    def test_double_file_type(self):
        """
        ph
        """
        self.assertEqual(self.App.get_file_type("wallpaper.png.zip"), ".zip")


class ConvertSize(unittest.TestCase):
    """
    Tests conversion of Bytes to Bytes, Kilobytes, Megabytes, Gigabytes,
    and Terabytes
    """

    def setUp(self):
        self.App = Cleaner(config="template_config.json")

    def test_convert_size(self):
        """
        Test that numbers between 0 and 5 are all even.
        """
        tests = {
            555: "555.0 B",
            568320: "555.0 KB",
            581959680: "555.0 MB",
            595926712320: "555.0 GB",
            610228953415680: "555.0 TB",
        }
        for bytes, bytes_string in tests.items():
            with self.subTest(bytes=bytes, bytes_string=bytes_string):
                result = self.App.convert_size(bytes)
                self.assertEqual(result, bytes_string)


class SetDestination(unittest.TestCase):
    def setUp(self):
        self.App = Cleaner(config="template_config.json")
        self.App.get_settings()

    def test_file_type_match(self):
        """
        ph
        """
        # video test
        result = self.App.set_destination("videofile.mp4")
        self.assertEqual(result, "C:/Downloads/Videos")
        # image test
        result = self.App.set_destination("photo.jpg")
        self.assertEqual(result, "C:/Downloads/Images")

    def test_keyword_match(self):
        """
        ph
        """
        result = self.App.set_destination("wallpaper.png")
        self.assertEqual(result, "C:/Downloads/Wallpapers")
        result = self.App.set_destination("python.py")
        self.assertEqual(result, "C:/Downloads/Coding/Python")

    def test_keyword_match_but_wrong_type(self):
        """
        test matching keyword with wrong file type
        """
        result = self.App.set_destination("python.mp4")
        self.assertEqual(result, "C:/Downloads/Videos")

    def test_special_case_match(self):
        """
        ph
        """
        result = self.App.set_destination("videofile.mkv")
        self.assertEqual(result, "C:/Downloads/HD Videos")


class SetupQueue(unittest.TestCase):
    def setUp(self):
        self.App = Cleaner(config="template_config.json")

    def test_main_run(self):
        """
        ph
        """
        self.App.watched_folder = "test/test folder"

        queue = self.App.setup_queue()
        answer = ""
        self.assertEqual(queue, answer)


class MoveFileQueue(unittest.TestCase):
    def setUp(self):
        self.App = Cleaner(config="template_config.json")

    def test_main_run(self):
        """
        ph
        """
        self.App.watched_folder = "test/test folder"
        self.App.setup_queue()
        self.App.move_file_queue()


class DeleteEmptyFolders(unittest.TestCase):
    """
    Tests delete_empty_folders function.
    """

    test_dir = "test/empty folders"

    def setUp(self):
        self.App = Cleaner(config="template_config.json")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def create_empty_folders(self, dir, folders):
        """
        Creates empty and non empty folders for testing.
        """
        # makes empty folders
        for folder in folders:
            path = f"{dir}/{folder}"
            os.makedirs(path)
        # makes non empty folder
        path = f"{dir}/Non Empty Folder"
        os.makedirs(path)
        with open(f"{path}/I exist.txt", "w") as f:
            f.write("Don't delete me!")

    def test_main_run(self):
        """
        ph
        """
        creat_folds = 6  # num of folders to create

        test_folders = [f"empty_{folder}" for folder in range(1, creat_folds)]
        self.create_empty_folders(self.test_dir, test_folders)

        # checks if correct num of folders were created
        total_folders = len(os.listdir(self.test_dir))
        self.assertEqual(creat_folds, total_folders)

        # runs test
        self.App.delete_empty_folders(self.test_dir)

        # verifies that test worked
        total_folders = len(os.listdir(self.test_dir))
        self.assertEqual(total_folders, 1)


if __name__ == "__main__":
    unittest.main()
