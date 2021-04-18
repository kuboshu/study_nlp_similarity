import sys
import os
sys.path.append(os.path.join('..', 'src'))
import utility
import unittest


class Test_get_pdflist(unittest.TestCase):
    def setUp(self):
        self.util = utility.Utility()
        self.test_dir = os.path.dirname(os.path.abspath(__file__))

    def test_exception(self):
        with self.assertRaises(utility.UtilityError):
            self.util.get_pdflist('.', -1)
        
    def test_getlist(self):
        result = self.util.get_pdflist('test_data')
        expected = [
            os.path.join(self.test_dir, 'test_data', 'smp00.pdf'),
            os.path.join(self.test_dir, 'test_data', 'smp01.pdf'),
            os.path.join(self.test_dir, 'test_data', 'smp02.pdf'),
            os.path.join(self.test_dir, 'test_data', 'smp03.pdf')
        ]
        self.assertListEqual(result, expected)

    def test_recursive(self):
        result = self.util.get_pdflist('test_data', recursive=True)
        expected = [
            os.path.join(self.test_dir, 'test_data', 'smp00.pdf'),
            os.path.join(self.test_dir, 'test_data', 'smp01.pdf'),
            os.path.join(self.test_dir, 'test_data', 'smp02.pdf'),
            os.path.join(self.test_dir, 'test_data', 'smp03.pdf'),
            os.path.join(self.test_dir, 'test_data', 'subdir', 'smp04.pdf'),
            os.path.join(self.test_dir, 'test_data', 'subdir', 'smp05.pdf'),
            os.path.join(self.test_dir, 'test_data', 'subdir', 'smp06.pdf'),
            os.path.join(self.test_dir, 'test_data', 'subdir', 'smp07.pdf')
        ]
        self.assertListEqual(result, expected)

    def test_limit(self):
        result = self.util.get_pdflist('test_data', limit=2)
        expected = [
            os.path.join(self.test_dir, 'test_data', 'smp00.pdf'),
            os.path.join(self.test_dir, 'test_data', 'smp01.pdf')
        ]
        self.assertListEqual(result, expected)

    def test_limit_01(self):
        """
        リミットのテスト
        再起的に検索した場合のリミットのテストです。
        """
        result = self.util.get_pdflist('test_data', limit=6, recursive=True)
        expected = [
            os.path.join(self.test_dir, 'test_data', 'smp00.pdf'),
            os.path.join(self.test_dir, 'test_data', 'smp01.pdf'),
            os.path.join(self.test_dir, 'test_data', 'smp02.pdf'),
            os.path.join(self.test_dir, 'test_data', 'smp03.pdf'),
            os.path.join(self.test_dir, 'test_data', 'subdir', 'smp04.pdf'),
            os.path.join(self.test_dir, 'test_data', 'subdir', 'smp05.pdf')
        ]
        self.assertListEqual(result, expected)

    def test_limit_02(self):
        """
        リミットのテスト
        ファイル数よりリミット値が大きい場合のテストです。
        """
        result = self.util.get_pdflist('test_data', limit=10, recursive=True)
        expected = [
            os.path.join(self.test_dir, 'test_data', 'smp00.pdf'),
            os.path.join(self.test_dir, 'test_data', 'smp01.pdf'),
            os.path.join(self.test_dir, 'test_data', 'smp02.pdf'),
            os.path.join(self.test_dir, 'test_data', 'smp03.pdf'),
            os.path.join(self.test_dir, 'test_data', 'subdir', 'smp04.pdf'),
            os.path.join(self.test_dir, 'test_data', 'subdir', 'smp05.pdf'),
            os.path.join(self.test_dir, 'test_data', 'subdir', 'smp06.pdf'),
            os.path.join(self.test_dir, 'test_data', 'subdir', 'smp07.pdf')
        ]
        self.assertListEqual(result, expected)

