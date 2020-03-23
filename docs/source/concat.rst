.. _concat:

Step 6: Concatenating samples
================================

.. _concat_intro:

Introduction
------------------

This optional step allows the concatenation of samples across multiple :term:`samples_batch` folders.

It can be used for LCI or LCIA arrays, and results can be saved in a new directory.

.. _concat_tech:

Technical reference
-----------------------------
``concat_samples_arrays_in_result_type_dir``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To concatenate LCI arrays or LCIA arrays for which the name of the folder is known, use
``concat_samples_arrays_in_result_type_dir``:

.. autofunction:: bw2preagg.concat_batches.concat_samples_arrays_in_result_type_dir

``concat_lcia_samples_arrays_from_method_tuple``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To concatenate LCIA arrays from a method tuple, use ``concat_lcia_samples_arrays_from_method_tuple``:

.. autofunction:: bw2preagg.concat_batches.concat_lcia_samples_arrays_from_method_tuple

