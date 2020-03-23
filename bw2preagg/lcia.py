from brightway2 import *
import numpy as np
from pathlib import Path
import warnings
import pickle
import pyprind
from .utils import get_ref_bio_dict_from_common_files, _check_result_dir, \
    _check_method, _get_lci_dir, load_LCI_array, load_det_lci, \
    _check_lci_missing, _check_project


def get_cf_with_indices(method, ref_bio_dict, project_name):
    """Extract row indices of biosphere matrix and associated cfs for given method

    A reference biosphere dictionary, associated with a given LCA object,
    must be supplied to ensure that the biosphere row indices are correct.

    Parameters
    ----------
    method: tuple
        Identification of the LCIA method, using Brightway2 tuple identifiers
    ref_bio_dict: dict
        Dictionary mapping elementary flow keys to matrix rows
    project_name : str
        Name of the brightway2 project where the database is imported

    Returns
    --------
    B_row_indices: list of int
        List of biosphere matrix row indices
    cfs: list of float
        List of associated characterization factors
    """
    # Switch to project
    if project_name is not None:
        projects.set_current(_check_project(project_name))
    # Load method
    loaded_method = Method(method).load()
    # Get characterized exchanges
    method_ordered_exchanges = [exc[0] for exc in loaded_method]
    # Collect row indices and cfs for characterized efs in LCI
    B_row_indices = []
    cfs = []
    for exc in method_ordered_exchanges: # For every exchange that has a characterization factor
        # Consider changing this https://stackoverflow.com/questions/16992713/translate-every-element-in-numpy-array-according-to-key
        try:
            # Check to see if it is in the bio_dict
            # If it is in ref_bio_dict, it is in the inventory
            B_row_indices.append(ref_bio_dict[exc]) # get index
            cfs.append(dict(loaded_method)[exc]) # get cf
        except:
            pass
    return B_row_indices, cfs


def calculate_lcia_array_from_arrays(
        LCI_array, B_row_indices, cfs,
        dtype=np.float32, return_total=True):
    """ Calculation of LCIA from array LCI array, B row indices and cfs

    Used by other functions to carry out actual calculations.

    Parameters
    ----------
    LCI_array: numpy array
        Life cycle inventory array, with rows equal to elementary flows
        and columns equal to separate LCI,
        e.g. from different MonteCarlo iterations
    B_row_indices: list of int
        List of biosphere matrix row indices
    cfs: list of float
        List of associated characterization factors
    dtype: str or dtype
        dtype to which the resulting LCIA array must be converted
    return_total: bool, default=True
        If True, sum LCIA array rows, returning total scores
        If False, returns an LCIA array with the same dimension as the LCI array

    Returns
    --------
    lcia_array: numpy.ndarray
        Array of LCIA scores
    """
    filtered_LCI_array = LCI_array[B_row_indices][:]
    cf_array = np.reshape(np.array(cfs), (-1, 1))
    lcia_array = (np.array(filtered_LCI_array) * cf_array)
    try:
        lcia_array = lcia_array.astype(dtype, copy=False)
    except:
        warnings.warn("Cannot convert LCIA array to dtype {}, will conserve dtype {}".format(dtype, str(lcia_array.dtype)))
    if return_total:
        return lcia_array.sum(axis=0)
    else:
        LCI_array_full = np.zeros(shape=LCI_array.shape)
        LCI_array_full[B_row_indices, :] = lcia_array
        return LCI_array_full


def calculate_lcia_array_from_activity_code(result_dir, act_code, method,
                                            samples_batch=0, dtype=np.float32,
                                            return_total=True, project_name=False):
    """ Retrieves LCI array and calculates LCIA array for a given method

    Parameters
    -----------
    result_dir : str
        Path to directory where results are stored
    act_code : str
        Code of the activity
    method : tuple
        LCIA method identification in brightway2 (tuple)
    samples_batch : int, default=0
        Integer id for sample batch. Used for campaigns names and for
        generating a seed for the RNG. The maximum value is 14.
    dtype : dtype or string, default=np.float32
        dtype the result should be converted to.
    return_total : bool, default=True
        If True, the function returns an array of total scores
        If False, the function returns an array of characterized elementary flows
    project_name : str
        Name of the brightway2 project where the database is imported
    """
    result_dir = Path(_check_result_dir(result_dir))
    lci_arr = load_LCI_array(result_dir, act_code, samples_batch)
    B_row_indices, cfs = get_cf_with_indices(
        method,
        get_ref_bio_dict_from_common_files(result_dir / "common_files"),
        project_name
    )
    return calculate_lcia_array_from_arrays(lci_arr, B_row_indices, cfs, dtype, return_total)


def save_all_lcia_score_arrays(result_dir, method, result_type='probabilistic',
                               samples_batch=0, dtype=np.float32,
                               return_total=True, return_per_exchange=True,
                               ignore_missing=True, project_name=None):
    """ Calculate and save LCIA score arrays for given set of LCI arrays and method

    Parameters
    ----------
    result_dir : str
        Path to directory where results are stored
    method : tuple
        LCIA method identification in brightway2 (tuple)
    result_type : str, default='probabilistic'
        Specify whether probabilistic or deterministic results should be generated
    samples_batch : int, default=0
        Integer id for sample batch. Used for campaigns names and for
        generating a seed for the RNG. The maximum value is 14.
    dtype : str or dtype
        dtype to which the resulting LCIA array must be converted
    return_total : bool, default=True
        If True, LCIA array with total scores across elementary flows are saved
    return_per_exchange : bool, default=None
        If True, LCIA array with scores per elementary flows are saved
    ignore_missing : bool, default=True
        If True, will calculate LCIA score arrays for all files in the
        corresponding LCI folder. If False, the calculation of LCIA score arrays
        will only proceed if all expected LCI arrays are found in the LCI array.
    project_name : str
        Name of the brightway2 project where the database is imported

    Returns
    -------
    None
    """
    result_dir = Path(_check_result_dir(result_dir))
    if project_name:
        projects.set_current(_check_project(project_name))
    method = _check_method(method)
    abbr = Method(method).get_abbreviation()
    try:
        LCI_dir = _get_lci_dir(result_dir, result_type, samples_batch, must_exist=True)
    except:
        raise ValueError("No {} LCI results, need to generate these first".format(result_type))
    if not ignore_missing:
        if not _check_lci_missing(result_dir):
            raise ValueError(
                "The expected LCI arrays and the LCI arrays in the LCI folder differ.")
    LCIA_dir = result_dir / result_type / abbr
    LCIA_dir.mkdir(exist_ok=True, parents=True)
    ref_bio_dict = get_ref_bio_dict_from_common_files(result_dir / "common_files")
    B_row_indices, cfs = get_cf_with_indices(method, ref_bio_dict, project_name)
    rev_ref_bio_dict = {v: k for k, v in ref_bio_dict.items()}
    exchange_keys = [rev_ref_bio_dict[k] for k in B_row_indices]
    LCIA_dir_common_files = LCIA_dir / "method_common_files"
    LCIA_dir_common_files.mkdir(exist_ok=True, parents=True)
    with open(LCIA_dir_common_files / "exchange_keys.pickle", "wb") as f:
        pickle.dump(exchange_keys, f)
    with open(LCIA_dir_common_files / "cfs.pickle", "wb") as f:
        pickle.dump(cfs, f)
    if return_total:
        total_LCIA_dir = LCIA_dir / "totals" / str(samples_batch)
        total_LCIA_dir.mkdir(exist_ok=True, parents=True)
    if return_per_exchange:
        per_exchange_LCIA_dir = LCIA_dir / "per_exchange" / str(samples_batch)
        per_exchange_LCIA_dir.mkdir(exist_ok=True, parents=True)
    fps_to_treat = [fp for fp in LCI_dir.iterdir()]
    for LCI_fp in pyprind.prog_bar(fps_to_treat):
        try:
            if not LCI_fp.is_file(): #Because there is sometimes a temp directory
                continue
            LCI_array = np.load(str(LCI_fp))
            LCIA_array = calculate_lcia_array_from_arrays(
                LCI_array, B_row_indices, cfs, dtype, return_total=False)
            if return_total:
                np.save(str(total_LCIA_dir / LCI_fp.name), LCIA_array.sum(axis=0).reshape(1, -1))
            if return_per_exchange:
                np.save(str(per_exchange_LCIA_dir / LCI_fp.name), LCIA_array.sum(axis=0))
        except Exception as err:
            print("Skipping {}: {}".format(LCI_fp.name, err))
    return None


def calculate_single_det_lcia_score(result_dir, act_code, method=None,
                                    B_row_indices=None, cfs=None):
    """ DEPRECATED Calculate LCIA array from dict of precalculated LCI results and method name

    Parameters
    -----------
    result_dir : str
        Path to directory where results are stored
    act_code : str
        Code of the activity
    method : tuple
        LCIA method identification in brightway2 (tuple)
    B_row_indices: list of int
        List of biosphere matrix row indices
    cfs: list of float
        List of associated characterization factors
    """
    if not any([method, B_row_indices, cfs]):
        raise ValueError("Must specify method tuple or indices and cfs")
    if not B_row_indices or not cfs:
        B_row_indices, cfs = get_cf_with_indices(
            method,
            get_ref_bio_dict_from_common_files(Path(result_dir) / "common_files")
        )
    lci_arr = load_det_lci(result_dir, act_code)
    return calculate_lcia_array_from_arrays(lci_arr, B_row_indices, cfs)


def save_det_lcia_scores(result_dir, method,
                         return_total=True, return_per_exchange=False,
                         ignore_missing=True):
    """ DEPRECATED Save dict of LCIA scores for all activities in database for given method

    Parameters
    -----------
    result_dir : str
        Path to directory where results are stored
    method : tuple
        LCIA method identification in brightway2 (tuple)
    """
    result_dir = Path(_check_result_dir(result_dir))
    B_row_indices, cfs = get_cf_with_indices(
        method,
        get_ref_bio_dict_from_common_files(result_dir / "common_files")
    )
    if not ignore_missing:
        if not _check_lci_missing(result_dir, result_type='deterministic'):
            raise ValueError(
                "The expected LCI arrays and the LCI arrays in the LCI folder differ.")

    lcia_dict = {
        code: calculate_lcia_array_from_arrays(lci_arr, B_row_indices, cfs, return_total)
        for code, lci_arr in det_lci_dict.items()
    }
    abbr = Method(method).get_abbreviation()
    save_dir = result_dir / "LCIA" /"deterministic_dicts"
    save_dir.mkdir(exist_ok=True, parents=True)
    with open(save_dir / "{}.pickle".format(abbr), "wb") as f:
        pickle.dump(lcia_dict, f)
    return None
