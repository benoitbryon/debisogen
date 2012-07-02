#########
debisogen
#########

Tools to automate creation of `Debian`_ Installer ISO images.


********
Abstract
********

debisogen was created to simplify creation and distribution of `Debian`_
"base systems":

* you focus on lightweight configuration;

* debisogen helps you generate custom `preseed files`_ via templates;

* debisogen produces a customized ISO image with the preseed and a
  base ISO image (typically an official ISO image).

* you can use the ISO image to automatically install a Debian system.

debisogen makes it possible to repeat a Debian installation from very
lightweight configuration.


*****
Usage
*****

Generate a preseed file with a template
=======================================

* Install requirements:

  * `Python`_ 2.6 or 2.7. You may use `Virtualenv`_ to get the adequate Python
    version.

* Install debisogen:

  ::

    pip install git+https://github.com/benoitbryon/debisogen.git#egg=debisogen

* Generate preseed file in ``var/`` directory:

  ::

    bin/paster create -t debian_preseed var/

  Answer questions. You get a ``var/preseed.cfg`` file.

.. note::

  You can generate files without interaction with paster. See paster's
  ``--config`` option and additional command line arguments. Full help with
  builtin ``paster help create`` command, or on `PasteScript`_ website.

Generate an ISO installer including the preseed file
====================================================

* Install requirements:

  * `Python`_ 2.6 or 2.7. You may use `Virtualenv`_ to get the adequate
    version.
  * Some additional shell commands (debisogen uses them):
  
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

    On a Debian system, you can achieve it with:

    ::

      sudo aptitude install curl bsdtar cpio mkisofs

* Install debisogen:

  ::

    pip install git+https://github.com/benoitbryon/debisogen.git#egg=debisogen

* Use provided ``debisogen`` command to generate ISO file:

  ::

    debisogen --help

  As another example, to combine remote `Debian Squeeze amd64 business card
  ISO`_ and `A custom FR preseed file for Debian Squeeze servers`_ to
  ``var/debian.iso`` file:

  ::

    debisogen --preseed=https://raw.github.com/benoitbryon/debisogen/master/etc/preseed-squeeze-server-fr.cfg --input-iso=http://cdimage.debian.org/debian-cd/6.0.5/amd64/iso-cd/debian-6.0.5-amd64-businesscard.iso --output-iso=var/debian.iso

  Obviously, you could be interested in using `the custom preseed file
  generated in previous section <#generate-a-preseed-file-with-a-template>`_.

Manually load preseed file in grub menu
=======================================

.. note::

  This feature is provided by the Debian installer itself, not by debisogen.
  It is documented here as an informational tip.

`A custom FR preseed file for Debian Squeeze servers`_ is provided in ``etc/``
directory. It defines following options:

* some fr_FR related configuration, such as locale, keyboard, mirror...
* root password will be prompted.
* no additional user account, i.e. you will have to create normal user account
  as root.
* partitionning: 512Mo swap, and the rest is / as ext4.
* install only standard utilities.

Usage:

* Boot a machine on a Debian Squeeze ISO, as an example `Debian Squeeze
  amd64 business card ISO`_.

* When you get to the install menu prompt, hit ESC, which will give you
  ``boot:`` prompt. At the prompt type:

  ::

    install auto=true priority=critical preseed/url=https://raw.github.com/benoitbryon/debisogen/master/etc/preseed-squeeze-server-fr.cfg

Put a preseed file on the network, to load it at boot time
==========================================================

.. note::

   This feature is provided by Python, not by debisogen. It is documented
   here as an informational tip.

You can use Python's builtin SimpleHttpServer to serve static files.
As an example, if you want to serve the sample preseed file provided at
``preseed-squeeze-server-fr.cfg`` on your machine:

::

  python -m SimpleHttpServer 8000

So you can access this preseed file at
http://YOUR-IP:8000/preseed-squeeze-server-fr.cfg

Then refer to `Manually load preseed file in grub menu`_ above to load this
preseed file with boot loader.


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

* Report and discuss issues or feature requests in the `bugtracker`_.

* Clone `code repository`_.

* Install development environment with ``make develop``.

* Run tests with ``make tests``.


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
.. _`preseed files`:
   http://www.debian.org/releases/squeeze/amd64/apb.html.en
.. _`Python`: http://python.org/
.. _`virtualenv`: http://virtualenv.org/
.. _`PasteScript`: http://pythonpaste.org/script/
.. _`Debian Squeeze amd64 business card ISO`:
   http://cdimage.debian.org/debian-cd/6.0.5/amd64/iso-cd/debian-6.0.5-amd64-businesscard.iso
.. _`a custom FR preseed file for Debian Squeeze servers`:
   https://raw.github.com/benoitbryon/debisogen/master/etc/preseed-squeeze-server-fr.cfg
.. _`bugtracker`: https://github.com/benoitbryon/debisogen/issues
.. _`code repository`: https://github.com/benoitbryon/debisogen
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
