.. _base_presamples:

Step 2: Generating base presamples
====================================

.. _base_presamples_intro:

Introduction
------------------

This step generates a :term:`presamples package` for all technosphere (**A**) and biosphere (**B**) elements for an
LCI database. The only function that the user needs for this step is ``generate_base_presamples``,
which is imported in the namespace with ``from bw2preagg import *``..

The resulting presample package is stored in the `presamples` subdirectory of the
:ref:`result_dir directory <file_structure>`. Information about the presamples packages are
stored in a :term:`presamples resource`, which are in turn included in a :term:`campaign`.

The :term:`samples_batch` argument (*int*) allows generating presamples in batches: each batch has its own presample
package, its own seed, and is associated with its own :term:`presamples resource` and :term:`campaign`.
Since the seed is determined from the samples_batch value, presample packages produced on different
computers are guaranteed to have the same values, increasing reproducibility of preaggregated LCI arrays and of LCA
results that are based on these arrays.

.. _base_presamples_tech:

Technical reference
-----------------------------

.. autofunction:: bw2preagg.generate_base_presample_resource.generate_base_presamples

