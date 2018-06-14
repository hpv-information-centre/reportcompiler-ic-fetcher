Report Compiler HPV Information Centre data fetcher
###################################################

|docs|

The Report Compiler HPV Information Centre data fetcher is a plugin for the Report Compiler
library that extends the MySQL fetcher to support the inclusion of sources, notes and other info
related to the fetched data. The plugin expects a particular database structure 
and it will be used in the HPV Information Centre project.

This project is being developed by the ICO/IARC Information Centre on HPV and Cancer 
and will be used in our report generation tasks.

.. image:: HPV_infocentre.png
   :height: 50px
   :align: center
   :target: http://www.hpvcentre.net

.. |docs| image:: https://readthedocs.org/projects/reportcompiler-ic-fetcher/badge/?version=develop
    :alt: Documentation Status
    :scale: 100%
    :target: https://reportcompiler-ic-fetcher.readthedocs.io/en/doc/?badge=develop

Features
============

* Transparent fetching of data associated with HPV Information Centre scientific data.
* Includes sources, notes, methods, years and dates for each table.
* Same interface as MySQL data fetcher.


Installation
============

Package
-------

.. code:: bash

 git clone https://github.com/hpv-information-centre/reportcompiler-ic-fetcher
 cd reportcompiler-ic-fetcher/scripts
 ./install_package.sh


Documentation
-------------

To generate HTML documentation:

.. code:: bash

 scripts/compile_docs.sh

This project uses Sphinx for documentation, so for other formats please use 'make' with the 
appropriate parameters on the doc directory.


Git hooks setup
---------------

.. code:: bash

 scripts/prepare_hooks.sh