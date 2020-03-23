.. _run_through:

Run-through: LCI and LCIA array production
===========================================

Scripts
-----------------------------

The easiest way to produce the required arrays is to use scripts found in a dedicated
github repository `here <https://github.com/PascalLesage/bw2-database-preaggregator-scripts>`_.
Simply download or clone the repository content on your computer.

Description of demo simulation for run-through
---------------------------------------------------

The general objective of this demo simulation is to:

  - generate and save two sets of 100 iteration LCI arrays for the ecoinvent v3.6 cutoff database.
    These samples should be balanced for water and land transformation exchanges
  - split the work as follows:

    - For the simulation on the Windows machine, all calculations are done within a *slice*, but across two sets of CPU
    - For the simulation on the computer cluster, calculations are done in 2 *slices*, and across four sets of CPU

  - generate and save corresponding LCIA arrays for three LCIA methods:

    - ('IPCC 2013', 'climate change', 'GWP 100a')
    - ('ReCiPe Midpoint (H) V1.13', 'water depletion', 'WDP')
    - ('ReCiPe Midpoint (H) V1.13', 'natural land transformation', 'NLTP')

  - Concatenate the LCIA scores across both samples batches and store these in a folder called "concat_preagg_demo".

.. _on_windows:

Sample simulation on a single Windows computer
------------------------------------------------

Install bw2preagg
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before being able to run the scripts, you need to install ``bw2preagg``. You should carry out the following operations
in a virtual environment.
In this run-through, I use a Conda environment, but you can substitute it with something else::

    conda create --name preagg_env python=3.7
    activate preagg_env

You can then install the package and all dependencies via pip::

    pip install bw2preagg

Modify parameter values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The parameters used by the various functions are centralized in the `params.txt` file,
found in the single_windows_machine folder of the scripts folder you downloaded from github.

The parameters are currently those used in the sample simulation.
You should review and modify as needed the parameter values.
The parameters are grouped in three sections:

  - Parameters that **must** be modified (e.g. filepaths)
  - Parameters that can safely be modified (e.g. number of iterations)
  - Parameters you should modify only if you know what you are doing

To modify the parameters, open the params.txt file in a text editor, make changes and save.


Running scripts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All the scripts to use are in the single_windows_machine folder of the scripts directory.
To use, simply activate the environment where bw2preagg was installed,
navigate to the *single_windows_machine* directory where the scripts can be found,
and launch the appropriate batch file::

    activate preagg_env
    cd path/to/scripts/single_windows_machine
    some_file.bat

You will be presented with the parameter values and asked to confirm that all is ok before proceeding.
Click ``Y`` to proceed if everything looks good.

Set-up project
^^^^^^^^^^^^^^^^^^^^

This creates the project, imports databases and generates common files as required.

You should set the following parameters in the ``params.txt`` file:

  - result_dir
  - database_dir
  - database_name
  - ecoinvent_version (limited to 3.4 and 3.6 for now)
  - project_name

Then, in the conda command prompt::

    activate preagg_env
    cd path/to/scripts/single_windows_machine
    setup_windows.bat

After running, all the files in the :ref:`common_files directory <file_structure>`
of the new ``result_dir`` should should have been added.

Base presamples generation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To create a presamples package for all **A** and **B** matrix elements.

You should set the :term:`iterations` and :term:`samples_batch` parameters in the `params.txt` file.

Then, in the conda command prompt::

    activate preagg_env
    cd path/to/scripts/single_windows_machine
    base_presamples_windows.bat

After running, there should be a new :term:`presamples package`  in the ``presamples`` subdirectory.

In the demo simulation, you would:

  - set ``iterations=100`` and ``samples_batch=0`` in `params.txt`, save and then run ``base_presamples_windows.bat``.
  - leave ``iterations=100`` and set ``samples_batch=1`` in `params.txt`, save and then rerun ``base_presamples_windows.bat``


Balancing presamples generation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This will create a presamples package for water and land transformation exchanges.

.. warning::
  This step takes a few hours. See the documentation on :ref:`balancing presamples <balancing_presamples_intro>`

In the conda command prompt::

    activate preagg_env
    cd path/to/scripts/single_windows_machine
    balancing_presamples_windows.bat

After running, there should be a new :term:`presamples package` in
the ``presamples`` subdirectory for land transformation and for water exchanges.

In the demo simulation, you would:

  - leave ``iterations=100`` and set ``samples_batch=0`` in `params.txt`, save and then run ``balancing_presamples_windows.bat``.
  - leave ``iterations=100`` and set ``samples_batch=1`` in `params.txt`, save and then rerun ``balancing_presamples_windows.bat``


Generate LCI arrays
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This will create LCI samples arrays.

.. warning::
  This step takes a several days!!! See the documentation on :ref:`generating LCI arrays <generating_LCI_intro>` for
  some strategies to keep time down. Therse calculations should be done on a dedicated computer or, better, on a
  :ref:`computer cluster <on_cluster>` .


You should set the ``parallel_jobs`` parameter in the ``params.txt`` file.

Then, in the conda command prompt::

    activate preagg_env
    cd path/to/scripts/single_windows_machine
    lci_windows.bat

After running this, there will be as many ``numpy.ndarray`` files stored in the subdirectory
result_dir/probabilistic/LCI/0 as there are activities in the database.
Each one has as many rows as elementary flows in the database, and as many columns as there are iterations.

In the demo simulation, you would:

  - set ``samples_batch=0`` and ``parallel_jobs=2`` in `params.txt`, save and then run ``lci_windows.bat``.
  - set ``samples_batch=1`` and leave ``parallel_jobs=2`` in `params.txt`, save and then rerun ``lci_windows.bat``.


Generate LCIA arrays
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The method for which you can calculate LCIA arrays are found in the ``/data/methods.json`` file of the
scripts directory. You select the method by setting the ``method_idx`` to the correct index value.
For example, for ("IPCC 2013", "climate change", "GWP 100a"), we have ``method_idx=714``.

Note that you can also *modify* the ``/data/methods.json`` file, but added methods should exist in the
project in which you are working and the integrity of the json file should not be corrupted.

By default, probabilistic LCIA arrays with total impacts are generated.
To generate LCIA arrays with results per elementary flow, set ``return_per_exchange=True``in
the single_windows_machine/params.txt file.
To generate deterministic LCIA arrays, set ``result_type=deterministic``.

Then, in the conda command prompt::

    activate preagg_env
    cd path/to/scripts/single_windows_machine
    lcia_windows.bat

In the demo simulation, you would:

  - set ``samples_batch=0`` and ``method_idx=714`` in `params.txt`, save and then run ``lcia_windows.bat``.
  - change ``samples_batch=1`` and leave ``method_idx=714`` in `params.txt`, save and then rerun ``lcia_windows.bat``.
  - redo the first two steps with ``method_idx=762`` (for water scarcity).
  - redo the first two steps with ``method_idx=756`` (for land transformation)


Concatenate LCIA arrays
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This will concatenate the LCIA scores generated above.

.. Note::
  When using these scripts, the concatenated arrays will always contain all samples_batches in the `result_dir`. To use
  only a subset of these, you will need to interact with the :ref:`function <concat_intro>`  directly.

You should set the following parameters in the `params.txt` file:

  - concat_result_type (LCI or LCIA)
  - method_idx
  - sim_name (name of folder in which to save arrays)
  - dest (destination of arrays)
  - fail_if_samples_batches_different (default=False)
  - ignore_missing_concat (default=False)

Then, in the conda command prompt::

    activate preagg_env
    cd path/to/scripts/single_windows_machine
    concat_windows.bat

In the demo simulation, you would:

  - set ``concat_result_type=LCIA``, ``method_idx=714``, ``sim_name=concat_preagg_demo`` and ``dest=some_valid_path`` in `params.txt`, save and then run ``concat_windows.bat``.
  - change ``method_idx=762`` (for water scarcity) and rerun ``concat_windows.bat``.
  - change ``method_idx=756`` (for water scarcity) and rerun ``concat_windows.bat``.

.. _on_cluster:

On a cluster
-----------------------------

Given the time required to generate the LCI samples, you should really use a computer cluster if you have access to one.

More detail to follow.
