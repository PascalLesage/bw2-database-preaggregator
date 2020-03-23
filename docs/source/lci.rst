.. _generating_LCI:

Step 4: Generating LCI samples
===========================================

.. _generating_LCI_intro:

Introduction
------------------

This step is where the actual LCI arrays are calculated. It works by successively instantiating as many
brightway2 ``MonteCarloLCA`` as there are activities in the LCI database, and calculating the resulting LCI results
for the same number of iterations as those contained in the corresponding presamples package.

What ensures that the LCI are *dependently* sampled is the use of presample packages, which inject the same
values for all technosphere (**A**) and biosphere (**B**) elements.

The resulting LCI arrays are stored in the `LCI` subdirectory of the :ref:`result_dir directory <file_structure>`.
Each :term:`samples_batch` has its own :ref:`subdirectory <file_structure>`

.. warning::
  Because of the large number of LCI datasets in LCI databases, this step is extremely long (on the order of days).
  ``bw2preagg`` implements three strategies to help reduce this time:

      1- :term:`samples_batch`: Allows calculating multiple sets of dependently sampled arrays with smaller number
      of iterations (one batch). These "batches" can then be concatenated into arrays with the required
      number of iterations.

      2- :term:`parallel_jobs`: Allows the parallel calculation of LCI arrays on multiple CPU of a given computer.

      3- :term:`slices`: Useful on computer clusters, allows further splitting up of the activity list into smaller slices
      and sending these to different jobs.

Several functions can be of interest, all pf which are imported in the namespace with ``from bw2preagg import *``.
The ``calculate_lci_array`` calculates the actual LCI arrays. It is rarely directly invoked by a user, but rather called
from ``set_up_lci_calculations``, that gathers the necessary information to run ``calculate_lci_array`` for a
specified set of activities. ``set_up_lci_calculations`` itself is rarely invoked direclty by a user, but rather from
a top-level ``dispatch_lci_calculators`` function that splits the LCI calculation across machines (:term:`slices`) and
across CPUs (:term:`parallel_jobs`).


.. _generating_LCI_tech:

Technical reference
-----------------------------

``dispatch_lci_calculators``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The top-level function is ``dispatch_lci_calculators``. It is typically the only one a user will interact with.

``dispatch_lci_calculators`` verifies that all required data (project, presamples, common files, etc.)
are actually available, splits the work first across slices (to run on multiple computers in a cluster)
and then across CPUs (to use MultiProcessing) and invokes ``set_up_lci_calculations``.

.. autofunction:: bw2preagg.lci.dispatch_lci_calculators

``set_up_lci_calculations``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``set_up_lci_calculations`` function then gathers the necessary information for the specified subset of activities
and invokes the subsequent ``calculate_lci_array`` for each activity for which LCI arrays need to be calculated.

.. autofunction:: bw2preagg.lci.set_up_lci_calculations

``calculate_lci_array``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``calculate_lci_array`` is the function where the actual LCI calculation occurs, using the brightway2 ``MonteCarloLCA``
class.

.. autofunction:: bw2preagg.lci.calculate_lci_array
