import unittest

from underrail_translation_kit.util.ul_path import UnderrailPath

class UnderrailPathTest(unittest.TestCase):

    def test_for_underrail_path_given(self):

        json_path = r"C:\SteamLibrary\steamapps\common\Underrail\data\dialogs\events\cc_gorskyassaultcrawlers.udlg"

        underrail_root = r"C:\SteamLibrary\steamapps\common\Underrail\data"
        json_root = r"C:\SteamLibrary\steamapps\common\Underrail\data"

        path = UnderrailPath(json_path, underrail_root, json_root)

        self.assertEqual(r"C:\SteamLibrary\steamapps\common\Underrail\data\dialogs\events\cc_gorskyassaultcrawlers.udlg.json",
                         path.json(),)
        self.assertEqual(r"C:\SteamLibrary\steamapps\common\Underrail\data\dialogs\events\cc_gorskyassaultcrawlers.udlg",
                         path.datafile())

    def test_for_json_path_given(self):

        underrail_path = r"C:\SteamLibrary\steamapps\common\Underrail\data\dialogs\events\cc_gorskyassaultcrawlers.udlg"

        underrail_root = r"C:\SteamLibrary\steamapps\common\Underrail\data"
        json_root = r"C:\SteamLibrary\steamapps\common\Underrail\data"

        path = UnderrailPath(underrail_path, underrail_root, json_root)

        self.assertEqual(r"C:\SteamLibrary\steamapps\common\Underrail\data\dialogs\events\cc_gorskyassaultcrawlers.udlg.json",
                         path.json(),)
        self.assertEqual(r"C:\SteamLibrary\steamapps\common\Underrail\data\dialogs\events\cc_gorskyassaultcrawlers.udlg",
                         path.datafile())


if __name__ == '__main__':
    unittest.main()
