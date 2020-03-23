bw2preagg
======================================

bw2preagg is used to generate dependently sampled LCI and LCIA arrays for whole databases.

It uses `Brightway2 framework <https://brightwaylca.dev/>`_ and `presamples <http://presamples.readthedocs.io/>`_.
The arrays are stored as ``numpy.ndarray`` files, and can be integrated in Brightway2 models using other modules
(`brightway2-aggregated <https://github.com/CIRAIG/brightway2-aggregated>`_,
`presamples <http://presamples.readthedocs.io/>`_).

The resulting result arrays allow the use of aggregated LCI or LCIA results (also known as cradle-to-gate results)
in LCA while also correctly integrating the uncertainty of LCI data, see
`Lesage et al. 2018 <https://doi.org/10.1007/s11367-018-1444-x>`_.

Generating samples of cradle-to-gate results for all activities in a database can be a lengthy process, especially
when dealing with large LCI databases like ecoinvent. The functions are therefore geared towards large, bulk
calculations, by e.g. facilitating multiprocessing and breaking down the task in multiple "batches" that can run on
different systems.

The samples are calculated in six steps:

:ref:`setup`
   Ready your system for sample generation: setup a brightway2 :term:`project`, import
   an ecoinvent database from ecoSpold files, and generate a number of files, stored in
   :ref:`common files directory <file_structure>`, that will be used by future steps.

:ref:`base_presamples`
  Generate a :term:`presamples package` for all **A** and **B** matrix elements. The presample package will have as many rows
  as there are matrix elements, and as many columns as the number of requested iterations. These will be injected in
  **A** and **B** matrices during LCI calculations in Step 4.

:ref:`balancing_presamples`
  (Optional) Generate a **balanced** :term:`presamples package` for water and another for land transformation exchanges.
  These are also injected in **A** and **B** matrices during LCI calculations in Step 4, overriding the base presamples
  from Step 2.

:ref:`generating_LCI`
  Generate LCI arrays for all activities in the database. These use the presamples packages from previous steps.

:ref:`generating_LCIA`
  (Optional) Transform the LCI arrays from Step 4 to arrays of LCIA scores.

:ref:`concat`
  (Optional) Concatenate LCI or LCIA arrays from multiple :term:`samples_batch` folders.


If you just want to run and calculate the samples, you can jump to the :ref:`run_through` section.

The most important concepts, input parameters and the structure of the output directory are summarized in the :ref:`Glossary`.

Table of contents
-------------------


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   setup_project
   base_presamples
   balancing_presamples
   lci
   lcia
   concat
   run_through
   glossary



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
