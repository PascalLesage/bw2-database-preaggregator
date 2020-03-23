.. _balancing_presamples:

Step 3: Generating balancing presamples
===========================================

Introduction
------------------

.. _balancing_presamples_intro:

Randomly sampling exchange values will usually break the intended balance across balances in a given activity (e.g.
the ratio of water in to water out for a given activity will be very different across Monte Carlo iterations).
This optional step generates balanced water and land transformation exchanges for a given LCI database,
and stores each in a dedicated :term:`presamples package`. The only function that the user needs
for this step is ``generate_balancing_presamples``, which is imported in the namespace with ``from bw2preagg import *``.

.. warning::
  The calculation of these balanced exchanges takes a long time (on the order of a few hours). However, it is only done
  once - this is the advantage of ``bw2preagg``.

The presamples packages are also stored in the `presamples` subdirectory of the
:ref:`result_dir directory <file_structure>`, and a corresponding :term:`presamples resource` is
added to a :term:`campaign` with the same :term:`samples_batch` id.

Balancing presamples are typically used to replace values in :ref:`base presamples <base_presamples>` with the
corresponding :term:`samples_batch` id during LCI calculations.

For more information on the balancing itself, consult the dedicated
`water exchange <https://github.com/CIRAIG/bw2waterbalancer>`_
and `land transformation <https://github.com/CIRAIG/bw2landbalancer>`_ exchange balancing packages.

.. _balancing_presamples_tech:

Technical reference
-----------------------------

.. autofunction:: bw2preagg.balancing_presamples.generate_balancing_presamples