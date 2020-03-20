.. _glossary:

Glossary
====================

Important arguments
---------------------

.. glossary::

    ``project_name``
        Name of the Brightway2 project where the LCI database and LCIA methods were imported and that contains the
        :term:`campaigns.db`.

    ``samples_batch``
        this is a definition

    ``some_other_arg``
        some other definition


Important concepts
----------------------

.. glossary::

    ``campaign``
        TODO


    ``campaigns.db``
        Database in Brightway2 project used to manage presample ressources. Used by ``bw2preagg`` to store paths to
        base and balancing presample resources associated with a given :term:`samples batch`.

    ``parallel_jobs``
        Multiprocessing...

    ``presamples package``
        TODO

    ``presamples resource``
        TODO

    ``project``
        `Brightway2 project <https://2.docs.brightway.dev/intro.html#projects>`_, which is a self-contained, top-level
        container for LCI data, LCIA methods, etc. used in Brightway2.

        Note: The argument :term:`project_name` refers to the Brightway2 project used by ``bw2preagg``.



    ``samples batch``
        You know...

    ``slices``
        slices

.. _file_structure:

Structure of the result_dir
------------------------------

.. code-block:: text

    ├── common_files
    │   ├── cgi1.py
    │   ├── cgi2.py
    │   ├── cgi3.py
    │   ├── README
    │   └── wiki.py
    ├── presamples
    │   ├── base_0 (base presamples package, sample_batch id=0)
    │   ├── water_0 (water exchange balancing presamples package, sample_batch id=0)
    │   ├── land_0 (land transformation exchange balancing presamples package, sample_batch id=0)
    │   ├── base_1
    │   ├── water_1
    │   └── land_1
    ├── LCI
    |   ├── 0 (sample_batch id = 0)
    │   │   ├── code_0.npy (=elementary flows, columns=iterations)
    │   │   ├── code_1.npy
    │   │   ├── code_2.npy
    │   │   ├── ...
    │   │   └── code_n.npy
    |   ├── 1 (sample_batch id)
    │   │   ├── code_0.npy
    │   │   ├── code_1.npy
    │   │   ├── code_2.npy
    │   │   ├── ...
    │   │   └── code_n.npy
    ├── LCIA
    │   ├── method_abbrev_0
    |   |   ├── 0 (sample_batch id)
    |   │   │   ├── code_0.npy
    |   │   │   ├── code_1.npy
    |   │   │   ├── code_2.npy
    |   │   │   ├── ...
    |   │   │   └── code_n.npy
    |   |   ├── 1 (sample_batch id)
    |   │   │   ├── code_0.npy
    |   │   │   ├── code_1.npy
    |   │   │   ├── code_2.npy
    |   │   │   ├── ...
    |   │   │   └── code_n.npy
    │   ├── method_abbrev_1
    |   |   ├── 0 (sample_batch id)
    |   │   │   ├── code_0.npy
    |   │   │   ├── code_1.npy
    |   │   │   ├── code_2.npy
    |   │   │   ├── ...
    |   │   │   └── code_n.npy
    |   |   ├── 1 (sample_batch id)
    |   │   │   ├── code_0.npy
    |   │   │   ├── code_1.npy
    |   │   │   ├── code_2.npy
    |   │   │   ├── ...
    |   │   │   └── code_n.npy
    │   ├── deterministic_dicts
    │   │   ├── method_abbrev_0.pickle
    │   │   ├── method_abbrev_1.pickle
