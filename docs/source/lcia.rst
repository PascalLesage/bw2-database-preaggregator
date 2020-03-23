.. _generating_LCIA:


Step 5: Generating LCIA samples
===========================================

.. _generating_LCIA_intro:

Introduction
------------------

This optional step converts the stored LCI arrays into method-specific arrays of LCIA scores.

LCIA arrays can be distinguished by:

  - number of columns:

     - **one column**: a deterministic results (``result_type=deterministic``)
     - **n columns**: one column per MonteCarlo iteration (use function ``result_type=probabilistic``)

  - number of rows:

     - **one row**: representing the sum of characterized elementary flows (``return_total=True``)
     - **m rows**: *m* characterized elementary flows (``return_per_exchange=True``).


While functions such as ``calculate_lcia_array_from_activity_code`` can calculate LCIA arrays for specific activities,
use ``save_all_lcia_score_arrays`` to generate and save LCIA arrays for all activities.

The resulting LCIA arrays are stored in a method-specific subdirectory of the :ref:`result_dir directory <file_structure>`.
The name of the subdirectory is a string *abbreviation* of the method name (see
`here <https://2.docs.brightway.dev/technical/bw2data.html#impact-assessment-data-stores>`_ for more detail on method
abbreviations). *Totals* and *per reference flow* are further separated in subdirectories, and finally
each :term:`samples_batch` has its own subdirectory.

.. note::  It is absolutely necessary to have access to the biosphere dictionary of the LCA object that was used to
  generate the samples, the :term:`ref_bio_dict`. It is stored in the :ref:`common_files <file_structure>`
  directory.

.. _generating_LCIA_tech:

Technical reference
-----------------------------

Top level functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``save_all_lcia_score_arrays``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: bw2preagg.lcia.save_all_lcia_score_arrays


``calculate_lcia_array_from_activity_code``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: bw2preagg.lcia.calculate_lcia_array_from_activity_code



Helper functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``get_cf_with_indices``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: bw2preagg.lcia.get_cf_with_indices


``calculate_lcia_array_from_arrays``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: bw2preagg.lcia.calculate_lcia_array_from_arrays


