.. _generating_LCIA:

Step 5: Generating LCIA samples
===========================================

.. _generating_LCIA_intro:

Introduction
------------------

This optional step converts the stored LCI arrays into method-specific arrays of LCIA scores.

    'calculate_all_det_LCIA_score',
    'save_all_LCIA_score_arrays',


The resulting LCIA arrays are stored in the `LCIA` subdirectory of the :ref:`result_dir directory <file_structure>`.
Each method has its own subdirectory, and inside each :term:`samples_batch` has its own subdirectory.

.. _generating_LCIA_tech:

Technical reference
-----------------------------

``get_cf_with_indices``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: bw2preagg.lcia.get_cf_with_indices

.. autofunction:: bw2preagg.lcia.calculate_LCIA_array_from_arrays

.. autofunction:: bw2preagg.lcia.calculate_LCIA_array_from_activity_code

.. autofunction:: bw2preagg.lcia.save_all_LCIA_score_arrays

.. autofunction:: bw2preagg.lcia.calculate_single_det_LCIA_score

.. autofunction:: bw2preagg.lcia.calculate_all_det_LCIA_score

