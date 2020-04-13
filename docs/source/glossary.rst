.. _glossary:

Glossary
====================

.. glossary::

    ``campaign``
        Collection of presample resources (ordered).

    ``campaigns.db``
        Database in Brightway2 project used to manage presample ressources. Used by ``bw2preagg`` to store paths to
        base and balancing presample resources associated with a given :term:`samples_batch`.

    ``parallel_jobs``
        Argument used in LCI generation function to determine how many parallel jobs to run on different CPUs of one
        computer.

    ``presamples package``
        Core data type of the presamples package. Folder containing data to inject in LCA matrices as well as matrix
        indices to identify where these data should be injected.

    ``presamples resource``
        Data on a presamples package, savec in ``campaigns.db``.

    ``project``
        `Brightway2 project <https://2.docs.brightway.dev/intro.html#projects>`_, which is a self-contained, top-level
        container for LCI data, LCIA methods, etc. used in Brightway2.

        Note: The argument :term:`project_name` refers to the Brightway2 project used by ``bw2preagg``.

    ``project_name``
        Name of the Brightway2 project where the LCI database and LCIA methods were imported and that contains the
        :term:`campaigns.db`.

    ``ref_bio_dict``
        Dictionary containing biosphere matrix row indices for elementary flows.

    ``samples_batch``
        A set of presamples, LCI arrays and LCIA arrays that are all generated from the same base data.
        Used to split out the work iteration-wise (e.g. calculate 5 batches of 1000 iterations rather than one
        batch of 5000 iterations). The total calculation time is not decreased, but it allows one to generate batches
        on different computers and makes results available, albeit perhaps with less iterations than required,
        more quickly.

    ``slices``
        Subset of activity codes to treat as a set. Used when using computer clusters to generate LCI arrays.

.. _file_structure:

Structure of the result_dir
------------------------------

.. code-block:: text

    ├── common_files
    │   ├── A_as_coo.xlsx (Row index, Col index, value for deterministic A matrix)
    │   ├── A_as_coo_scipy.pickle (deterministic A matrix as SciPy sparse COO matrix)
    │   ├── activity_dict.pickle
    │   ├── B_as_coo.xlsx (Row index, Col index, value for deterministic B matrix)
    │   ├── B_as_coo_scipy.pickle (deterministic B matrix as SciPy sparse COO matrix)
    │   ├── bio_dict.pickle
    │   ├── biosphere_description.xlsx (description of elementary flows in B matrix, per row index)
    │   ├── cfs.npy (array with characterization factors, methods as columns and elementary flows as rows)
    │   ├── cfs.xlsx (same as cfs.npy, but in Excel, with method names in columns)
    │   ├── IO_Mapping.pickle
    │   ├── ordered_activity_codes.json
    │   ├── product_dict.pickle
    │   └── technosphere_description.xlsx (description of products/activities in A matrix, per index)
    ├── presamples
    │   ├── base_0 (base presamples package, samples_batch id=0)
    │   ├── water_0 (water exchange balancing presamples package, samples_batch id=0)
    │   ├── land_0 (land transformation exchange balancing presamples package, samples_batch id=0)
    │   ├── base_1
    │   ├── water_1
    │   ├── land_1
    │   └── ...
    ├── deterministic
    │   ├── LCI
    |   |   ├── 0 (sample_batch id = 0)
    |   │   │   ├── activity_code_0.npy (rows=elementary flows, columns=iterations)
    │   │   │   ├── activity_code_1.npy
    │   │   │   ├── activity_code_2.npy
    │   │   │   ├── ...
    │   │   │   └── activity_code_n.npy
    |   │   ├── 1 (sample_batch id)
    │   │   │   ├── activity_code_0.npy
    │   │   │   ├── activity_code_1.npy
    │   │   │   ├── activity_code_2.npy
    │   │   │   ├── ...
    │   │   │   └── activity_code_n.npy
    │   ├── LCIA
    │   │   ├── method_abbrev_0
    │   │   |   ├── totals
    │   │   |   |   ├── 0 (sample_batch id)
    │   │   |   │   │   ├── code_0.npy
    │   │   |   │   │   ├── code_1.npy
    │   │   |   │   │   ├── code_2.npy
    │   │   |   │   │   ├── ...
    │   │   |   │   │   └── code_n.npy
    │   │   |   |   ├── 1 (sample_batch id)
    │   │   |   │   │   ├── code_0.npy
    │   │   |   │   │   ├── code_1.npy
    │   │   |   │   │   ├── code_2.npy
    │   │   |   │   │   ├── ...
    │   │   |   │   │   └── code_n.npy
    │   │   |   ├── per_exchange
    │   │   |   |   ├── 0 (sample_batch id)
    │   │   |   │   │   ├── code_0.npy
    │   │   |   │   │   ├── code_1.npy
    │   │   |   │   │   ├── code_2.npy
    │   │   |   │   │   ├── ...
    │   │   |   │   │   └── code_n.npy
    │   │   |   |   ├── 1 (sample_batch id)
    │   │   |   │   │   ├── code_0.npy
    │   │   |   │   │   ├── code_1.npy
    │   │   |   │   │   ├── code_2.npy
    │   │   |   │   │   ├── ...
    │   │   |   │   │   └── code_n.npy
    ├── probabilistic
    │   ├── LCI
    |   |   ├── 0 (sample_batch id = 0)
    |   │   │   ├── activity_code_0.npy (rows=elementary flows, columns=iterations)
    │   │   │   ├── activity_code_1.npy
    │   │   │   ├── activity_code_2.npy
    │   │   │   ├── ...
    │   │   │   └── activity_code_n.npy
    |   │   ├── 1 (sample_batch id)
    │   │   │   ├── activity_code_0.npy
    │   │   │   ├── activity_code_1.npy
    │   │   │   ├── activity_code_2.npy
    │   │   │   ├── ...
    │   │   │   └── activity_code_n.npy
    │   ├── LCIA
    │   │   ├── method_abbrev_0
    │   │   |   ├── totals
    │   │   |   |   ├── 0 (sample_batch id)
    │   │   |   │   │   ├── code_0.npy
    │   │   |   │   │   ├── code_1.npy
    │   │   |   │   │   ├── code_2.npy
    │   │   |   │   │   ├── ...
    │   │   |   │   │   └── code_n.npy
    │   │   |   |   ├── 1 (sample_batch id)
    │   │   |   │   │   ├── code_0.npy
    │   │   |   │   │   ├── code_1.npy
    │   │   |   │   │   ├── code_2.npy
    │   │   |   │   │   ├── ...
    │   │   |   │   │   └── code_n.npy
    │   │   |   ├── per_exchange
    │   │   |   |   ├── 0 (sample_batch id)
    │   │   |   │   │   ├── code_0.npy
    │   │   |   │   │   ├── code_1.npy
    │   │   |   │   │   ├── code_2.npy
    │   │   |   │   │   ├── ...
    │   │   |   │   │   └── code_n.npy
    │   │   |   |   ├── 1 (sample_batch id)
    │   │   |   │   │   ├── code_0.npy
    │   │   |   │   │   ├── code_1.npy
    │   │   |   │   │   ├── code_2.npy
    │   │   |   │   │   ├── ...
    │   │   |   │   │   └── code_n.npy
