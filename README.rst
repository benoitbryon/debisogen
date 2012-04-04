##########################
marmelune.debianisobuilder
##########################

Custom scripts, files and templates around `Debian`_ installer.

.. warning::

  This is **experimental** work.

********
Abstract
********

Tools provided here were created to simplify creation and distribution of
`Debian`_ "base systems":

* automate installation of a Debian system on a machine.
* preconfigure parts or full Debian installation.
* distribute ISO files, based on existing Debian's ISO files.
* or distribute only configuration files (a preseed file or a configuration
  file for a preseed file generator).

The original context was to simplify and standardize creation of servers,
mostly virtual machines, for web development:

* share server configuration in a team.
* share something lightweight, like a "business-card ISO installer" or (even
  better) a configuration file, rather than big disk images.
* rely on something repeatable, not on a
  big-disk-image-nobody-knows-how-to-rebuild-exactly-the-same (TM).
* allow configuration from the beginning, i.e. share a system but allow
  users to customize some points, such as passwords or network configuration.

*****
Usage
*****

Manually load preseed file in grub menu
=======================================

`A custom FR preseed file for Debian Squeeze servers`_ is provided in ``etc/``
directory. It defines following options:

* some fr_FR related configuration, such as locale, keyboard, mirror...
* root password will be prompted.
* no additional user account, i.e. you will have to create normal user account
  as root.
* partitionning: 512Mo swap, and the rest is / as ext4.
* install only standard utilities.

Usage:

* Download a Debian Squeeze iso at `Debian download page`_, as an example
  `Debian Squeeze amd64 business card ISO`_.
* Boot your server on the ISO.
* When you get to the install menu prompt, hit ESC, which will give you boot:
  prompt. At the prompt type:

  ::

    install auto=true priority=critical preseed/url=https://raw.github.com/benoitbryon/marmelune.debianisobuilder/master/etc/preseed-squeeze-server-fr.cfg

Generate a preseed file with a template
=======================================

* Install requirements:

  * `Python`_ 2.6 or 2.7
  * `Git`_, or you will have to download sources as archive on
    `marmelune.debianisobuilder's repository`_.

* Install marmelune.debianisobuilder:

  .. highlight:: sh

  ::

    git clone
    cd marmelune.debianisobuilder
    python lib/buildout/bootstrap.py --distribute
    bin/buildout -N

* Generate preseed file:

  .. highlight:: sh

  ::

    bin/paster create -t marmelune_debian_preseed ./var/preseed

  Answer questions. You got a ``./var/preseed/preseed-server-fr.cfg`` file.

.. note::

  You can generate files without interaction with paster. See paster's
  ``--config`` option and additional command line arguments. Full help with
  builtin ``paster help create`` command, or on `PasteScript`_ website.

Put a preseed file on the network, to load it at boot time
==========================================================

You can use Python's builtin SimpleHttpServer to serve static files.
As an example, if you want to serve the sample preseed file provided here at
``etc/preseed-squeeze-server-fr.cfg`` on your machine:

.. highlight:: sh

::

  cd etc/
  python -m SimpleHttpServer 8000

So you can access this preseed file at
http://YOUR-IP:8000/preseed-squeeze-server-fr.cfg

Then refer to "Manually load preseed file in grub menu" above to load this
preseed file with boot loader.

Generate an ISO installer including the preseed file
====================================================

* Install requirements:

  * `Python`_ 2.6 or 2.7
  * `Git`_, or you will have to download sources as archive on
    `marmelune.debianisobuilder's repository`_.
  * Some additional shell commands:
  
    * curl (only if you use remote ISO or preseed file)
    * bsdtar
    * chmod
    * gunzip
    * cd
    * cpio
    * gzip
    * find
    * md5sum
    * mkisofs

    On Debian systems, you can:

    .. highlight:: sh

    ::

      sudo aptitude install curl bsdtar cpio mkisofs

* Install marmelune.debianisobuilder:

  .. highlight:: sh

  ::

    git clone
    cd marmelune.debianisobuilder
    python lib/buildout/bootstrap.py --distribute
    bin/buildout -N

* Use provided ``debianisobuilder`` command to generate ISO file:

  .. highlight:: sh

  ::

    bin/debianisobuilder --help

  As an example, to combine remote `Debian Squeeze amd64 business card ISO`_
  and `A custom FR preseed file for Debian Squeeze servers`_ to
  ``var/debian.iso`` file:

  .. highlight:: sh

  ::

    bin/debianisobuilder --preseed=https://raw.github.com/benoitbryon/marmelune.debianisobuilder/master/etc/preseed-squeeze-server-fr.cfg --input-iso=http://cdimage.debian.org/debian-cd/6.0.4/amd64/iso-cd/debian-6.0.4-amd64-businesscard.iso --output-iso=var/debian.iso

************
Alternatives
************

These tools are really simple ones, and may stay simple. They were created as
a proof of concept and so they satisfy very simple needs. If you are looking
for more powerful tools, fetch the web. Advanced tools to create custom Debian
distributions and deploy them should exist...

**********
Contribute
**********

* Install package as told in "Generate an ISO installer including the preseed
  file" section above.
* Install development environment:

  .. highlight:: sh

  ::

    bin/buildout -N install dev-environment

* Run tests:

  .. highlight:: sh

  ::

    bin/nosetests --with-coverage --rednose --with-doctest src/

.. note::

  ``marmelune`` namespace is related to http://marmelune.net/. Here, it is used
  as a personal namespace for experimental work. If you think this package
  should be promoted, open a ticket and propose a package name.

**********
References
**********

* `Debian Squeeze documentation about preseeding`_
* `Debian Squeeze preseed example file`_
* `HOWTO automate Debian installs with preseed`_, where the preseeding file is
  loaded on the network using grub options.
* `How to modify an existing Debian installer CD image`_
* `Simple CD and image cookbook`_
* `How to view, modify and recreate initrd.img`_
* `Documentation of partman-auto recipes`_

.. target-notes::

.. _`Debian`: http://debian.org/
.. _`a custom FR preseed file for Debian Squeeze servers`:
   https://raw.github.com/benoitbryon/marmelune.debianisobuilder/master/etc/preseed-squeeze-server-fr.cfg
.. _`Debian download page`: http://www.debian.org/distrib/
.. _`Debian Squeeze amd64 business card ISO`:
   http://cdimage.debian.org/debian-cd/6.0.4/amd64/iso-cd/debian-6.0.4-amd64-businesscard.iso
.. _`Python`: http://python.org/
.. _`Git`: http://git-scm.org/
.. _`marmelune.debianisobuilder's repository`:
   https://github.com/benoitbryon/marmelune.debianisobuilder
.. _`PasteScript`: http://pythonpaste.org/script/
.. _`Debian Squeeze documentation about preseeding`:
   http://www.debian.org/releases/squeeze/amd64/apb.html.en
.. _`Debian Squeeze preseed example file`:
   http://www.debian.org/releases/squeeze/example-preseed.txt
.. _`HOWTO automate Debian installs with preseed`:
   http://fak3r.com/2011/08/18/howto-automate-debian-installs-with-preseed
.. _`How to modify an existing Debian installer CD image`:
   http://wiki.debian.org/DebianInstaller/Modify/CD
.. _`Simple CD and image cookbook`:
   http://www.debian-administration.org/articles/273
.. _`How to view, modify and recreate initrd.img`:
   http://www.thegeekstuff.com/2009/07/how-to-view-modify-and-recreate-initrd-img/
.. _`Documentation of partman-auto recipes`:
   http://dev.blankonlinux.or.id/browser/nanggar/debian-installer/doc/devel/partman-auto-recipe.txt?rev=nanggar%2Cdebian-installer%2C1
