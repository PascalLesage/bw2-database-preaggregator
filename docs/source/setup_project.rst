.. _setup:

Step 1: Setup
===============

.. _setup_intro:

Introduction
------------------

Setting things up to use ``bw2preagg`` is done through a single function, ``setup_project``,
which is imported in the namespace with ``from bw2preagg import *``.
This function does multiple things to ready your system for sample generation:

   - sets up a brightway2 :term:`project`. To use an existing project, simply pass ``overwrite_project=False``
   - imports an ecoinvent database from ecoSpold files. To use an existing imported LCI database, simply pass
     ``overwrite_database=False``. If the database does not exist in the project, or if ``overwrite_database=True``, you
     must pass a valid path ``database_dir`` pointing to a directory with ecoSpold2 files.
   - generates a number of files that are used later and store these in the
     `common_files` subdirectory of the :ref:`result_dir directory <file_structure>`.
     To skip generation of these files if they exist already, simply pass ``force_write_common_files=False``.
   - generates deterministic LCI results for all activities, stored in the
     `deterministic` subdirectory of the :ref:`result_dir directory <file_structure>`.


.. _setup_tech:

Technical reference
-----------------------------

.. autofunction:: bw2preagg.setup_project.setup_project


