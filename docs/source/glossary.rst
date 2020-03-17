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

    ``campaigns.db``
        Database in Brightway2 project used to manage presample ressources. Used by ``bw2preagg`` to store paths to
        base and balancing presample resources associated with a given :term:`samples batch`.

    ``presample packages``
        TODO

    ``project``
        `Brightway2 project <https://2.docs.brightway.dev/intro.html#projects>`_, which is a self-contained, top-level
        container for LCI data, LCIA methods, etc. used in Brightway2.

        Note: The argument :term:`project_name` refers to the Brightway2 project used by ``bw2preagg``.



    ``samples batch``
        You know...



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
    │   ├── cgi3.py
    │   ├── cgi3.py
    │   ├── cgi3.py
    │   └── cgi3.py


