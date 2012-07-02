"""Unit tests."""
import os
from unittest import TestCase

from debisogen.iso import toggle_boot_loader
from debisogen.utils import use_temp_dir


class ToggleBootLoaderTestCase(TestCase):
    def test_file_content(self):
        with use_temp_dir() as iso_directory:
            os.mkdir(os.path.join(iso_directory, 'isolinux'))
            filename = os.path.join(iso_directory, 'isolinux', 'isolinux.cfg')
            sample_content = """
some  options
and somewhere
timeout 0
or
timeout   0
or
    timeout 0 # some comments
but not timeout 0"""
            expected_content = """
some  options
and somewhere
timeout 1
or
timeout   1
or
    timeout 1 # some comments
but not timeout 0"""
            with open(filename, 'w') as file:
                file.write(sample_content)
            toggle_boot_loader(iso_directory, True)
            with open(filename) as file:
                real_content = file.read()
        self.assertEqual(real_content, expected_content)
