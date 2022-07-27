import unittest

from underrail_translation_kit.unpacker import unpack_as_stream
from underrail_translation_kit.msnrbf_parser import parse_binary_stream
from tests.msnrbf_parser.helper import assertEqualToStream, assertEndOfStream

""""
単体テストではないが、
過去、特に問題を引き起こしたファイルを読んでテストする
"""

class ProbolematicFilesTest(unittest.TestCase):

    def do_test_at_file(self, path):
        with unpack_as_stream(path) as f:
            result = parse_binary_stream(f)
            assertEqualToStream(self, result.raw_bytes, f)
            assertEndOfStream(self, f)

    def test_read_advancedhealthhypo_gzip(self):
        self.do_test_at_file("msnrbf_parser/data/problematic/advancedhealthhypo.item")

    def test_read_bigbret_udlg(self):
        self.do_test_at_file("msnrbf_parser/data/problematic/bigbret1.udlg")

    def test_read_boltquiver(self):
        self.do_test_at_file("msnrbf_parser/data/problematic/boltquiver")

    def test_read_ch_edgar_udlg(self):
        self.do_test_at_file("msnrbf_parser/data/problematic/ch_edgar.udlg")

    def test_read_ferryman_udlg(self):
        self.do_test_at_file("msnrbf_parser/data/problematic/ferryman.udlg")

    def test_read_hoddurform(self):
        self.do_test_at_file("msnrbf_parser/data/problematic/hoddurform")

    def test_read_shotggunshell_12(self):
        self.do_test_at_file("msnrbf_parser/data/problematic/shotgunshell_12")

    def test_read_superhealthhypo(self):
        self.do_test_at_file("msnrbf_parser/data/problematic/superhealthhypo")

    def test_read_utilities_k(self):
        self.do_test_at_file("msnrbf_parser/data/problematic/utilities.k")

    def test_read_feats_k(self):
        self.do_test_at_file("msnrbf_parser/data/problematic/feats.k")

    def test_read_cc_forgerpretguard_udlg(self):
        self.do_test_at_file("msnrbf_parser/data/problematic/cc_forgerpretguard.udlg")

if __name__ == '__main__':
    unittest.main()
