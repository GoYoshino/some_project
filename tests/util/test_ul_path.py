import unittest

from underrail_translation_kit.util.ul_path import UnderrailPath

class UnderrailPathTest(unittest.TestCase):

    def test_for_underrail_path_given(self):

        underrail_path = r"C:\SteamLibrary\steamapps\common\Underrail\data\dialogs\events\cc_gorskyassaultcrawlers.udlg"

        underrail_root = r"C:\SteamLibrary\steamapps\common\Underrail\data"
        json_root = r"D:\underrail_json\data"

        path = UnderrailPath(underrail_path, underrail_root, json_root)

        self.assertEqual(r"D:\underrail_json\data\dialogs\events\cc_gorskyassaultcrawlers.udlg.json",
                         path.json(),)
        self.assertEqual(r"C:\SteamLibrary\steamapps\common\Underrail\data\dialogs\events\cc_gorskyassaultcrawlers.udlg",
                         path.datafile())

    def dtest_for_json_path_given(self):

        underrail_path = r"C:\SteamLibrary\steamapps\common\Underrail\data\dialogs\events\cc_gorskyassaultcrawlers.udlg"

        underrail_root = r"C:\SteamLibrary\steamapps\common\Underrail\data"
        json_root = r"D:\underrail_json\data"
        patch_root = r"D:\patch\data"

        path = UnderrailPath(underrail_path, underrail_root, json_root, patch_root)

        self.assertEqual(r"D:\underrail_json\data\dialogs\events\cc_gorskyassaultcrawlers.udlg.json",
                         path.json(),)
        self.assertEqual(r"C:\SteamLibrary\steamapps\common\Underrail\data\dialogs\events\cc_gorskyassaultcrawlers.udlg",
                         path.datafile())
        self.assertEqual(r"D:\patch\data\dialogs\events\cc_gorskyassaultcrawlers.udlg",
                         path.patch())


if __name__ == '__main__':
    unittest.main()
