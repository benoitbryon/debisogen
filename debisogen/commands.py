"""Shell commands."""
from optparse import OptionParser  # Python 2.6 and 2.7 compatibility.
                                   # Optparse has deprecated status in 2.7.
                                   # Replaced by argparse.
import os
import tempfile

from iso import download_iso_file, insert_preseed_into_iso
from utils import is_url, download_file


def build_iso():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("--input-iso",
                      help="Path or URL to ISO file. Default is 'input.iso'.",
                      action="store", type="string", dest="input_iso",
                      default='input.iso')
    parser.add_option("--output-iso",
                      help="Path to ISO to generate. Default is 'output.iso'.",
                      action="store", type="string", dest="output_iso",
                      default='output.iso')
    parser.add_option("--preseed", help="Path or URL to preseed file. " \
                      "Default is 'preseed.cfg'.", action="store",
                      type="string", dest="preseed_file",
                      default='preseed.cfg')
    parser.add_option("--hide-boot-loader", help="Hide boot loader (default).",
                      action='store_true', dest="is_boot_loader_hidden",
                      default=True)
    parser.add_option("--show-boot-loader", help="Show boot loader.",
                      action='store_false', dest="is_boot_loader_hidden")
    (options, args) = parser.parse_args()

    tmp_input_iso = None
    tmp_preseed_file = None
    try:
        # Download ISO file if necessary.
        if is_url(options.input_iso):
            file_handle, tmp_input_iso = tempfile.mkstemp()
            download_iso_file(options.input_iso, tmp_input_iso)
            options.input_iso = tmp_input_iso
        # Download preseed file if necessary.
        if is_url(options.preseed_file):
            file_handle, tmp_preseed_file = tempfile.mkstemp()
            download_file(options.preseed_file, tmp_preseed_file)
            options.preseed_file = tmp_preseed_file
        # Check that input files exist.
        if not os.path.exists(options.preseed_file):
            parser.error('No such preseed file %s' % options.preseed_file)
        if not os.path.exists(options.input_iso):
            parser.error('No such input ISO %s' % options.input_iso)
        # Build ISO!
        insert_preseed_into_iso(options.preseed_file, options.input_iso,
                                options.output_iso,
                                options.is_boot_loader_hidden)
        if os.path.exists(options.output_iso):
            print "SUCCESS: %s file has been generated." % options.output_iso
    finally:
        if tmp_input_iso:
            os.unlink(tmp_input_iso)
        if tmp_preseed_file:
            os.unlink(tmp_preseed_file)
