from brightway2 import *
import numpy as np
from pathlib import Path
import warnings
from .utils import get_ref_bio_dict_from_common_files

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
    lca_specific_biosphere_indices: list of int
        List of biosphere matrix row indices
    cfs: list of float
        List of associated characterization factors
    """
    # Load method
    loaded_method = Method(method).load()
    # Get characterized exchanges
    method_ordered_exchanges = [exc[0] for exc in loaded_method]
    # Collect row indices and cfs for characterized efs in LCI
    lca_specific_biosphere_indices = []
    cfs = []
    for exc in method_ordered_exchanges: # For every exchange that has a characterization factor
        # Consider changing this https://stackoverflow.com/questions/16992713/translate-every-element-in-numpy-array-according-to-key
        try:
            # Check to see if it is in the bio_dict
            # If it is in ref_bio_dict, it is in the inventory
            lca_specific_biosphere_indices.append(ref_bio_dict[exc]) # get index
            cfs.append(dict(loaded_method)[exc]) # get cf
        except:
            pass
    return lca_specific_biosphere_indices, cfs

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


def calculate_LCIA_array(code, result_dir, samples_batch, method, dtype=np.float32, return_total=True):
    """ Calculate LCIA array from LCI array path and method name"""
    lci_arr = np.load(str(Path(result_dir)/"lci"/samples_batch/"{}.npy".format(code)))
    indices, cfs = get_cf_with_indices(method, get_ref_bio_dict_from_common_files(Path(result_dir)/"common_files"))
    return calculate_LCIA_array_from_arrays(lci_arr, indices, cfs, dtype, return_total)


def calculate_LCIA_RESULT_FOR_DET(det_lca_dict, code, method, result_dir):
    """ Calculate LCIA array from LCI array path and method name"""
    lci_arr = det_lca_dict[code]
    indices, cfs = get_cf_with_indices(method, get_ref_bio_dict_from_common_files(Path(result_dir)/"common_files"))
    return calculate_LCIA_array_from_arrays(lci_arr, indices, cfs)
