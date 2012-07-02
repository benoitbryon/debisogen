"""Utilities and shell command to bundle a preseed file inside a Debian ISO."""
import glob
import os
import re
import shutil
import subprocess

from utils import use_temp_dir, replace_in_file, execute_command, download_file


def download_iso_file(source, destination):
    """Download system installer image from source to destination."""
    download_file(source, destination)


def iso_to_directory(iso_file, directory):
    """Extract content of an ISO image to destination directory."""
    if not os.path.exists(directory):
        os.makedirs(directory)
    execute_command('bsdtar -C %(directory)s -xf %(iso_file)s',
                    {'directory': directory, 'iso_file': iso_file})
    execute_command('chmod -R u+w %(directory)s', {'directory': directory})


def directory_to_iso(directory, iso_file):
    """Create ISO image from directory."""
    output_dir = os.path.dirname(os.path.abspath(iso_file))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    execute_command('mkisofs -o %(iso)s -r -J -no-emul-boot ' \
                    ' -boot-load-size 4 -boot-info-table ' \
                    '-b isolinux/isolinux.bin -c isolinux/boot.cat %(dir)s',
                    {'iso': iso_file, 'dir': directory})


def initrd_to_directory(initrd_file, directory):
    """Extract initrd.gz file to destination subdirectory."""
    assert(initrd_file.endswith('.gz'))
    execute_command('gunzip %(file)s', {'file': initrd_file})
    initrd_file = initrd_file[:-3]
    execute_command('cd %(dir)s ; cpio -id < %(file)s', {'dir': directory,
                                                         'file': initrd_file})


def directory_to_initrd(directory, initrd_file):
    """Compress directory as initrd.gz file."""
    assert(initrd_file.endswith('.gz'))
    initrd_file = initrd_file[:-3]
    execute_command("cd %(in)s && find . | cpio --create --format='newc' > " \
                    "%(out)s", {'in': directory, 'out': initrd_file})
    execute_command('gzip %(file)s', {'file': initrd_file})


def toggle_boot_loader(directory, is_boot_loader_hidden=True):
    """In directory, alter isolinux.cfg file to hide (default) or show boot
    loader on startup.

    Hiding boot loader is required for a fully automated installation.
    """
    timeout = int(is_boot_loader_hidden)  # 1 to hide boot loader!
    # Replace "timeout" option in isolinux/isolinux.cfg
    filename = os.path.join(directory, 'isolinux', 'isolinux.cfg')
    pattern = r'^(\s*timeout\s*)[0-1](\s*#|$)'
    flags = re.IGNORECASE
    pattern = re.compile(pattern, flags)
    replacement = '\g<1>%d\g<2>' % timeout
    replace_in_file(pattern, replacement, filename)


def rebuild_md5sum(directory):
    """Rebuild md5sum.txt file in the given directory."""
    execute_command('cd %(dir)s ; md5sum `find ! -name "md5sum.txt" ! ' \
                    '-path "./isolinux/*" -follow -type f` > md5sum.txt ;',
                    {'dir': directory})


def insert_preseed_into_iso(preseed_file, input_iso_file, output_iso_file,
                            is_boot_loader_hidden=True):
    """Alters input ISO file to create another ISO file which includes preseed
    file."""
    input_iso_file = os.path.normpath(os.path.abspath(input_iso_file))
    with use_temp_dir() as iso_directory:
        iso_to_directory(input_iso_file, iso_directory)
        # Find adequate install directory, i.e. "install.amd" for amd64
        # architecture.
        install_dir = glob.glob(os.path.join(iso_directory, 'install.*'))
        if not install_dir:
            raise Exception('No install.* directory found in %(iso)s')
        if len(install_dir) > 1:
            raise Exception('Several install.* directories found in %(iso)s ' \
                            'ISO: %(dirs)s' % {'iso': input_iso_file,
                                               'dirs': install_dir})
        initrd_file = os.path.join(install_dir[0], 'initrd.gz')
        with use_temp_dir() as initrd_directory:
            initrd_to_directory(initrd_file, initrd_directory)
            output_preseed_file = os.path.join(initrd_directory, 'preseed.cfg')
            shutil.copy(preseed_file, output_preseed_file)
            directory_to_initrd(initrd_directory, initrd_file)
        toggle_boot_loader(iso_directory, is_boot_loader_hidden)
        rebuild_md5sum(iso_directory)
        directory_to_iso(iso_directory, output_iso_file)
