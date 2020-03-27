from brightway2 import *
from .utils import _check_project, _check_database, _check_result_dir, \
    missing_useful_files, _get_campaign, get_ref_bio_dict_from_common_files, _get_lci_dir

import numpy as np
import os
import time
import multiprocessing as mp
from pathlib import Path
from math import ceil
import json
import presamples


def calculate_lci_array(database_name, act_code, presamples_paths, g_dimensions,
                        total_iterations, g_samples_dir):
    """Return LCI array using specified presamples for given activity

    Typically invoked from generate_LCI_samples.set_up_lci_calculations

    Parameters
    --------------
    database_name : str
        Name of the LCI database
    act_code : str
        code of the activity
    presamples_paths : list
        list of paths to presamples packages
    g_dimensions : int
        Number of rows in biosphere matrix
    total_iterations : int
        Number of iterations (i.e. number of columns in presample arrays)
    g_samples_dir : str
        Path to directory where LCI arrays will be saved

    Returns
    ---------
    None
    """

    lci = np.memmap(
        filename=str(g_samples_dir / "temp" / "{}.npy".format(act_code)),
        dtype="float32",
        mode='w+',
        shape=(g_dimensions, total_iterations)
    )
    act = get_activity((database_name, act_code))
    mc = MonteCarloLCA({act: act['production amount']}, presamples=presamples_paths)
    for i in range(total_iterations):
        try:
            next(mc)
            this_g = np.squeeze(np.array(mc.inventory.sum(axis=1)))
            assert this_g.size == g_dimensions
            lci[:, i] = this_g
        except Exception as err:
            print("***********************\nactivity {} problem with iteration {}:{}".format(
                act_code, i, err)
            )
            lci[:, i] = np.full(g_dimensions, np.nan).ravel()
    lci_as_arr = np.array(lci)
    assert lci_as_arr.shape == (g_dimensions, total_iterations), "Dimension not ok: {}".format(lci_as_arr.shape)
    del lci
    (Path(g_samples_dir) / "temp" / "{}.npy".format(act_code)).unlink()
    np.save(str(g_samples_dir / "{}.npy".format(act_code)), lci_as_arr)
    lci_as_arr = None  # Explicitly free up memory


def set_up_lci_calculations(activity_list, result_dir, worker_id, database_name,
                            samples_batch, project_name):
    """Dispatch LCI calculation for a list of activities

    Parameters
    --------------
    activity_list : list
        List of codes to activities for which LCI arrays should be calculated
    result_dir : str
        Path to directory where results are stored
    worker_id : int
        Identification of the worker if using MultiProcessing, used only for
        error messages.
    database_name : str
        Name of the LCI database
    samples_batch : int
        Integer id for sample batch. Used for campaigns names and for
        generating a seed for the RNG. The maximum value is 14.
    project_name : str
        Name of the brightway2 project where the database is imported

    Returns
    ---------
    None
    """
    projects.set_current(_check_project(project_name))
    g_samples_dir = _get_lci_dir(result_dir, 'probabilistic', samples_batch, must_exist=False)
    g_samples_dir_temp = g_samples_dir / "temp"
    g_samples_dir_temp.mkdir(exist_ok=True, parents=True)

    ref_bio_dict = get_ref_bio_dict_from_common_files(Path(result_dir) / "common_files")
    campaign = _get_campaign(str(samples_batch), expect_base_presamples=True)
    presample_paths = [p for p in campaign]
    assert presample_paths
    pps = [presamples.PresamplesPackage(p) for p in presample_paths]
    iterations = list(set([pp.ncols for pp in pps]))
    assert len(iterations) == 1
    total_iterations = iterations[0]
    print("Worker ID {}, requested iterations: {}".format(worker_id, total_iterations))

    g_dimensions = len(ref_bio_dict)
    times = []
    for act_i, act_code in enumerate(activity_list):
        t0 = time.time()
        try:
            calculate_lci_array(
                database_name, act_code, presample_paths, g_dimensions, total_iterations, g_samples_dir)
            times.append(time.time() - t0)
        except Exception as err:
            print("************Failure for {} by {}: {}************".format(act_code, worker_id, err))
    print("Worker ID: {}\n\tTotal of {} LCIs of {} iterations"
          "\n\tTotal time: {} minutes\n\tAverage time: {} minutes per LCI".format(
        worker_id, len(activity_list), total_iterations, sum(times) / 60, (sum(times) / len(times)) / 60
    ))


def techno_dicts_equal(ref_techno_dict, new_techno_dict):
    """ Returns True if two product or activity dicts are functionally equivalent

    Difference in database name are ignored.
    """
    ref_techno_dict_for_comparison = {k[1]: v for k, v in ref_techno_dict.items()}
    new_techno_dict_for_comparison = {k[1]: v for k, v in new_techno_dict.items()}
    return ref_techno_dict_for_comparison == new_techno_dict_for_comparison


def get_techno_dicts_translator(ref_techno_dict, new_techno_dict):
    """ Return dict where k, v are resp. indices in reference and new techno matrix

    Applicable to both products (rows in A matrix) and
    activities (columns in A and B matrices)
    The names of the databases do not need to be the same, but the codes
    should be common
    """
    ref_bd_name = list(ref_techno_dict.keys())[0][0]
    new_bd_name = list(new_techno_dict.keys())[0][0]
    return {ref_techno_dict[(ref_bd_name, k[1])]: new_techno_dict[(new_bd_name, k[1])] for k in
            new_techno_dict.keys()}


def dispatch_lci_calculators(project_name, database_name, result_dir, samples_batch=0,
                             parallel_jobs=1, slice_id=None, number_of_slices=None):
    """ Dispatches LCI array calculations to distinct processes (multiprocessing)

    If number_of_slices/slice_id are not None, then only a subset of database activities are processed.

    The number of iterations is determined by the number of columns in the
    presample packages referenced in the corresponding campaign.

    If slice_id and number_of_slices are not None, will only treat a subset of activities.

    Parameters
    -----------
    project_name : str
        Name of the brightway2 project where the database is imported
    database_name : str
        Name of the LCI database
    result_dir : str
        Path to directory where results are stored
    samples_batch : int, default=0
        Integer id for sample batch. Used for campaigns names and for
        generating a seed for the RNG. The maximum value is 14.
    parallel_jobs : int, default=1
        Number of parallel jobs to run using multiprocessing
    slice_id : int, default=None
        ID of slice. Useful when calculations are split across many computers or jobs on a computer cluster.
        If None, LCI arrays are generated for all activities in the database.
    number_of_slices : int, default=None
        Number of slices over which the calculations are split.
        Useful when calculations are split across many computers or jobs on a computer cluster.
        If None, LCI arrays are generated for all activities in the database.
    """
    print("\n\n**************Dispatching LCI CALCULATORS**************\n\n")
    # Ensure base data exist and are valid
    projects.set_current(_check_project(project_name))
    _check_database(database_name)
    result_dir = Path(_check_result_dir(result_dir))
    missing_files = missing_useful_files(result_dir)
    if missing_files:
        raise ValueError("Missing files: ", missing_files)
    _get_campaign(samples_batch, expect_base_presamples=True)

    # Create directory for LCI arrays
    g_master_dir = result_dir / "probabilistic" / "LCI"
    g_master_dir.mkdir(exist_ok=True, parents=True)
    g_samples_dir = g_master_dir / "{}".format(samples_batch)
    g_samples_dir.mkdir(exist_ok=True)

    chunks = lambda l, n: [l[i:i + n] for i in range(0, len(l), n)]

    # Identify subset of activities to treat
    with open(result_dir / "common_files" / "ordered_activity_codes.json", 'r') as f:
        all_activity_codes = json.load(f)
    print("Total number of activities in database: ", len(all_activity_codes))
    if slice_id is None or number_of_slices is None:
        activity_codes = all_activity_codes
        print("Number of activities to treat in single slice: {}".format(
            len(activity_codes)))
    else:
        activity_codes = chunks(all_activity_codes, ceil(len(all_activity_codes) / (number_of_slices)))[slice_id]
        print("Number of activities to treat in slice {} of {}: {}".format(
            slice_id, number_of_slices, len(activity_codes)))
    activities_to_treat = []
    for act in activity_codes:
        lci_filename = "{}.npy".format(act)
        # Check if this result has already been generated
        if lci_filename in os.listdir(g_samples_dir):
            # And make sure all columns were filled in with results
            if not any(np.load(str(g_samples_dir / lci_filename), mmap_mode='r').sum(axis=0) == 0):
                # If all done, then go on to the next activity
                continue
        else:
            activities_to_treat.append(act)
    if not activities_to_treat:
        print("No lci arrays to generate, exiting")
        return
    else:
        print("Total of {} lci arrays to generate".format(len(activities_to_treat)))

    activity_sublists = chunks(activities_to_treat, ceil(len(activities_to_treat) / parallel_jobs))
    print("LCI generation dispatched in {} chunks with the following number of activities to treat: {}".format(
        len(activity_sublists), str([len(x) for x in activity_sublists])))
    workers = []
    for i, s in enumerate(activity_sublists):
        j = mp.Process(target=set_up_lci_calculations,
                       args=(s, result_dir, i, database_name, samples_batch, project_name)
                       )
        workers.append(j)
    for w in workers:
        w.start()
    for w in workers:
        w.join()
