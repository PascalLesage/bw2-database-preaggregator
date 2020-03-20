import os
from brightway2 import *
import numpy as np
from pathlib import Path
import warnings
import pickle
import json
from .utils import get_ref_bio_dict_from_common_files, _check_result_dir, \
    _check_method, _get_LCI_dir, load_LCI_array, _get_det_lci_dict


def get_cf_with_indices(method, ref_bio_dict):
    """Extract row indices of biosphere matrix and associated cfs for given method

    A reference biosphere dictionary, associated with a given LCA object,
    must be supplied to ensure that the biosphere row indices are correct.

    Parameters
    ----------
    method: tuple
        Identification of the LCIA method, using Brightway2 tuple identifiers
    ref_bio_dict: dict
        Dictionary mapping elementary flow keys to matrix rows

    Returns
    --------
    B_row_indices: list of int
        List of biosphere matrix row indices
    cfs: list of float
        List of associated characterization factors
    """
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


def calculate_LCIA_array_from_arrays(
        LCI_array, B_row_indices, cfs,
        dtype=np.float32, return_total=True):
    """ Calculate LCIA from LCI array and specific B row indices and cfs

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
    lcia_array: numpy array
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


def calculate_LCIA_array_from_activity_code(result_dir, act_code, method,
                                            samples_batch=0, dtype=np.float32,
                                            return_total=True):
    """ Calculate LCIA array from LCI array path and method name

    Parameters
    -----------
    result_dir : str
        Path to directory where results are stored
    act_code : str
        Code of the activity
    method : tuple
        LCIA method identification in brightway2 (tuple)
    sample_batch : int, default=0
        Integer id for sample batch. Used for campaigns names and for
        generating a seed for the RNG. The maximum value is 14.
    dtype : dtype or string, default=np.float32
        dtype the result should be converted to.
    return_total : bool, default=True
        If True, the function returns an array of total scores
        If False, the function returns an array of characterized elementary flows
    """
    result_dir = Path(_check_result_dir(result_dir))
    lci_arr = load_LCI_array(result_dir, act_code, samples_batch)
    B_row_indices, cfs = get_cf_with_indices(method, get_ref_bio_dict_from_common_files(result_dir / "common_files"))
    return calculate_LCIA_array_from_arrays(lci_arr, B_row_indices, cfs, dtype, return_total)


def save_all_LCIA_score_arrays(result_dir, method, samples_batch=0,
                               dtype=np.float32, return_total=True,
                               ignore_missing=True):
    """ Calculate and save LCIA score arrays for all activities in database

    Parameters
    ----------
    result_dir : str
        Path to directory where results are stored
    method : tuple
        LCIA method identification in brightway2 (tuple)
    sample_batch : int, default=0
        Integer id for sample batch. Used for campaigns names and for
        generating a seed for the RNG. The maximum value is 14.
    dtype : str or dtype
        dtype to which the resulting LCIA array must be converted
    return_total : bool, default=True
        If True, sum LCIA array rows, returning total scores
        If False, returns an LCIA array with the same dimension as the LCI array
    ignore_missing : bool, default=True
        If True, will calculate LCIA score arrays for all files in the
        corresponding LCI folder. If False, the calculation of LCIA score arrays
        will only proceed if all expected LCI arrays are found in the LCI array.

    Returns
    -------
    None
    """
    result_dir = Path(_check_result_dir(result_dir))
    method = _check_method(method)
    abbr = Method(method).get_abbreviation()
    LCI_dir = _get_LCI_dir(result_dir, samples_batch)
    LCIA_dir = result_dir / "LCIA" / abbr / str(samples_batch)
    LCIA_dir.mkdir(exist_ok=True, parents=True)
    if not return_total:
        LCIA_dir = LCIA_dir / "per_exchange"
    if not ignore_missing:
        with open(result_dir / "common_files" / "ordered_activity_codes.json", "r") as f:
            expected_activity_codes = json.load(f)
        available = sorted([f[0:-4] for f in os.listdir(LCI_dir)])
        if not sorted(expected_activity_codes) == available:
            raise ValueError(
                "The expected LCI arrays and the LCI arrays in the LCI folder differ.")
    ref_bio_dict = get_ref_bio_dict_from_common_files(result_dir / "common_files")
    B_row_indices, cfs = get_cf_with_indices(method, ref_bio_dict)
    if not return_total:
        rev_ref_bio_dict = {v: k for k, v in ref_bio_dict.items()}
        exchange_keys = [rev_ref_bio_dict[k] for k in B_row_indices]
        LCIA_dir_common_files = LCIA_dir / "common_files"
        LCIA_dir_common_files.mkdir(exist_ok=True, parents=True)
        with open(LCIA_dir_common_files / "exchange_keys.pickle", "wb") as f:
            pickle.dump(exchange_keys, f)
        with open(LCIA_dir_common_files / "cfs.pickle", "wb") as f:
            pickle.dump(cfs, f)
    for LCI_fp in LCI_dir.iterdir():
        LCI_array = np.load(str(LCI_fp))
        LCIA_array = calculate_LCIA_array_from_arrays(
            LCI_array, B_row_indices, cfs, dtype, return_total)
        np.save(str(LCIA_dir / LCI_fp.name), LCIA_array)
    return None


def calculate_single_det_LCIA_score(result_dir, act_code, method=None,
                                    B_row_indices=None, cfs=None,
                                    det_lci_dict=None):
    """ Calculate LCIA array from dict of precalculated LCI results and method name

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
    det_lci_dict : dict, default=None
        Dictionary with activity codes as keys and LCI arrays as values.
        If None, the dictionary will be loaded from common_files
    """
    if not any([method, B_row_indices, cfs]):
        raise ValueError("Must specify method tuple or indices and cfs")
    if not B_row_indices or not cfs:
        B_row_indices, cfs = get_cf_with_indices(
            method,
            get_ref_bio_dict_from_common_files(Path(result_dir) / "common_files")
        )
    if not det_lci_dict:
        det_lci_dict = _get_det_lci_dict(result_dir)
    lci_arr = det_lci_dict[act_code]
    return calculate_LCIA_array_from_arrays(lci_arr, B_row_indices, cfs)


def calculate_all_det_LCIA_score(result_dir, method, det_lci_dict=None, save_to_result_dir=True):
    """ Calculate dict of LCIA scores for all activities in database for given method

    Parameters
    -----------
    result_dir : str
        Path to directory where results are stored
    method : tuple
        LCIA method identification in brightway2 (tuple)
    det_lci_dict : dict, default=None
        Dictionary with activity codes as keys and LCI arrays as values.
        If None, the dictionary will be loaded from common_files
    save_to_result_dir : bool, default=True
        If True, save resulting dict to result_dir
    """
    result_dir = Path(_check_result_dir(result_dir))
    B_row_indices, cfs = get_cf_with_indices(
        method,
        get_ref_bio_dict_from_common_files(result_dir / "common_files")
    )
    if not det_lci_dict:
        det_lci_dict = _get_det_lci_dict(result_dir)
    lcia_dict = {
        code: calculate_LCIA_array_from_arrays(lci_arr, B_row_indices, cfs)
        for code, lci_arr in det_lci_dict.items()
    }
    if save_to_result_dir:
        abbr = Method(method).get_abbreviation()
        save_dir = result_dir / "LCIA" /"deterministic_dicts"
        save_dir.mkdir(exist_ok=True, parents=True)
        with open(save_dir / "{}.pickle".format(abbr), "wb") as f:
            pickle.dump(lcia_dict, f)
    return lcia_dict
