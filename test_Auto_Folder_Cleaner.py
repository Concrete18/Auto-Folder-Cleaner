from Auto_Folder_Cleaner import Cleaner
from unittest.mock import patch
import unittest
import json
import time
import os

class TestAFC(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        files = ['videofile.mkv', 'wallpaper.png', 'python.mp4', 'python.py', 'wallpaper.png.zip', 'installer.exe']
        cls.main_dir = os.getcwd()
        cls.test_dir = os.path.join(cls.main_dir, 'testing')
        if not os.path.exists(cls.test_dir):
            os.makedirs(cls.test_dir)
        os.chdir(os.path.join(cls.main_dir, 'testing'))
        for _file in files:
            if not os.path.isfile(_file):
                with open(_file, "x")  as f:
                    f.write("Test Text")
        cls.files = {}
        for _file in os.scandir(cls.test_dir):
            cls.files[_file.name] = _file
        os.chdir(cls.main_dir)


    @classmethod
    def tearDownClass(cls):
        for _file in os.scandir(cls.test_dir):
            if os.path.exists(_file.path) and not os.path.isfile(_file.path):
                os.rmdir(_file.path)
            else:
                os.remove(_file.path)
        os.rmdir(cls.test_dir)

    # FIXME File_Move function.
    # def test_File_Move(self):
    #     hd_video_dir = os.path.join(self.test_dir, 'HD Video')
    #     File_Move(self.files['videofile.mkv'], hd_video_dir)
    #     self.assertTrue(os.path.exist(os.path.join(self.test_dir, 'HD Video', 'videofile.mkv')))


    def test_Set_Destination(self):
        App = Cleaner()
        self.watched_folder = 'C:/Downloads'
        # Tests for correct file destination being returned properly based on json config.
        self.assertEqual(App.Set_Destination(self.files['videofile.mkv']), "C:/Downloads/HD Videos")
        self.assertEqual(App.Set_Destination(self.files['wallpaper.png']), "C:/Downloads/Wallpapers")
        self.assertEqual(App.Set_Destination(self.files['python.mp4']), "C:/Downloads/Videos")
        self.assertEqual(App.Set_Destination(self.files['python.py']), "C:/Downloads/Coding/Python")


    def test_Get_File_Type(self):
        App = Cleaner()
        # Tests Get_File_Type function to be sure it works with a variety of file names.
        self.assertEqual(App.Get_File_Type(self.files['wallpaper.png']), ".png")
        self.assertEqual(App.Get_File_Type(self.files['wallpaper.png.zip']), ".zip")

    # FIXME Mock input in Delete_Check function.
    # def test_Delete_Check(self):
    #     # Tests to see if function asks to delete files in delete_def.
    #     self.assertEqual(Set_Destination('C:/Downloads', self.files['installer.exe']), "skip")


if __name__ == '__main__':
    unittest.main()
