##########################
marmelune.debianisobuilder
##########################

Custom scripts, files and templates around `Debian`_ installer.

.. warning::

  This is **experimental** work.

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

This tool is not released yet.

************
Alternatives
************

These tools are really simple ones, and may stay simple. They were created as
a proof of concept and so they satisfy very simple needs. If you are looking
for more powerful tools, fetch the web. Advanced tools to create custom Debian
distributions and deploy them should exist...

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
