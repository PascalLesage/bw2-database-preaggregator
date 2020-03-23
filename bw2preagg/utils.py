from pathlib import Path
import math
from brightway2 import *
import presamples
import pickle
import numpy as np
import json
import os


def missing_useful_files(result_dir):
    """Return list of missing useful files"""
    useful_files = [
        'ordered_activity_codes.json',  # activity codes
        'product_dict.pickle',  # lca.product_dict
        'bio_dict.pickle',  # lca.biosphere_dict
        'activity_dict.pickle',  # lca.activity_dict
        #'tech_params.pickle',  # lca.tech_params
        #'bio_params.pickle',  # lca.bio_params
        'IO_Mapping.pickle',  # mapping
        #'tech_row_indices.npy',  # NO LONGER NEEDED
        #'tech_col_indices.npy',  # NO LONGER NEEDED
        #'bio_row_indices.npy',  # NO LONGER NEEDED
        #'bio_col_indices.npy'  # NO LONGER NEEDED
    ]

    if not (Path(result_dir)/"common_files").is_dir():
        return useful_files

    return [
        file for file in useful_files
        if not (Path(result_dir)/"common_files"/file).is_file()
    ]


def _check_project(project_name):
    """ Check that project already exists and has been set up

    Returns project name if all checks pass"""
    if project_name not in projects:
        raise ValueError(
            "Project {} does not exist, run setup_project first".format(
                project_name
            )
        )
    projects.set_current(project_name)
    if "biosphere" not in databases and "biosphere3" not in databases:
        raise ValueError(
            "Project {} has not been set up, run setup_project first".format(
                project_name
            )
        )
    return project_name


def _check_database(database_name):
    """Check that database is in project and that it has activities

    Returns database_name if all checks pass"""
    if database_name not in databases:
        raise ValueError(
            "Database {} has not been set up, run setup_project first".format(
                database_name
            )
        )
    if len(Database(database_name))==0:
        raise ValueError(
            "Database {} is empty, run setup_project with "
            "overwrite_database=True".format(
                database_name
            )
        )
    return database_name


def _check_method(method):
    """Check that the method exists in brightway2 project"""
    if not method in methods:
        raise ValueError("{} is not a valid method in project {}".format(method, projects.current))
    return method


def _check_result_dir(result_dir):
    """Check that result_dir exists"""
    if not Path(result_dir).is_dir():
        raise ValueError("result_dir {} does not exist".format(result_dir))
    return result_dir


def _get_campaign(samples_batch, expect_base_presamples=False):
    """ Return campaign for given samples_batch"""
    campaign = presamples.Campaign.get_or_none(
        presamples.Campaign.name == "c{}".format(samples_batch)
    )
    if not campaign:
        if expect_base_presamples:
            raise ValueError(
                "No base campaign generated yet, run "
                "generate_base_presample_resource first"
            )
        else:
            campaign = presamples.Campaign.create(name="c{}".format(samples_batch))
            campaign.save()
    return campaign


def _get_lci_dir(result_dir, result_type='probabilistic', samples_batch=None, must_exist=True):
    """Return LCI directory path if it exists else raise ValueError"""
    result_dir = Path(_check_result_dir(result_dir))
    if result_type == 'probabilistic':
        LCI_dir = result_dir / result_type / "LCI" / str(samples_batch)
    elif result_type == 'deterministic':
        LCI_dir = result_dir / result_type / "LCI"
    else:
        raise ValueError("Result type {} not valid".format(result_type))
    if not LCI_dir.is_dir():
        if must_exist:
            raise ValueError("No directory at {}".format(LCI_dir))
        else:
            LCI_dir.mkdir(parents=True)
    return LCI_dir


def _get_lcia_dir(result_dir, samples_batch, method, must_exist=True):
    """Return LCI directory path if it exists else raise ValueError"""
    result_dir = Path(_check_result_dir(result_dir))
    method = _check_method(method)
    abbr = Method(method).get_abbreviation()
    LCIA_dir = result_dir / "LCIA" / abbr / str(samples_batch)
    if not LCIA_dir.is_dir():
        if must_exist:
            raise ValueError("No directory at {}".format(LCIA_dir))
        else:
            LCIA_dir.mkdir(parents=True)
    return LCIA_dir


def _get_det_lci_dict(result_dir):
    """Load det_lci_dict"""
    result_dir = Path(_check_result_dir(result_dir))
    det_lci_dict_fp = result_dir / "common_files" / "det_lci_dict.pickle"
    if not det_lci_dict_fp.is_file():
        raise ValueError("No det_lci_dict.pickle file found in common_files folder")
    with open(det_lci_dict_fp, "rb") as f:
        det_lci_dict = pickle.load(f)
    return det_lci_dict


def _get_det_lcia_dict(result_dir, method):
    """Load dict with LCIA scores"""
    result_dir = _check_result_dir(result_dir)
    method = _check_method(method)
    abbr = Method(method).get_abbreviation()
    det_lcia_dict_fp = result_dir / "LCIA" / "deterministic_dicts" / "{}.pickle".format(abbr)
    if not det_lcia_dict_fp.is_file():
        raise ValueError("No det_lcia_dict.pickle file found in common_files folder")
    with open(det_lcia_dict_fp, "rb") as f:
        det_lcia_dict = pickle.load(f)
    return det_lcia_dict


def load_LCI_array(result_dir, act_code, samples_batch=0):
    """Return existing LCI array

    Parameters
    -----------
    result_dir : str
        Path to directory where results are stored
    act_code : str
        Code of the activity
    samples_batch : int, default=0
        Integer id for sample batch. Used for campaigns names and for
        generating a seed for the RNG. The maximum value is 14.

    Returns
    --------
    LCI samples : numpy.ndarray
        LCI samples, with rows = elementary flows and columns = iterations
    """
    LCI_dir = Path(_get_lci_dir(result_dir, samples_batch))
    arr_fp = LCI_dir / "{}.npy".format(act_code)
    if not arr_fp.is_file():
        raise ValueError("File {} does not exist".format(arr_fp))
    return np.load(str(arr_fp))


def load_LCIA_array(result_dir, act_code, method, samples_batch=0):
    """Return existing LCIA array

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

    Returns
    --------
    LCIA samples : numpy.ndarray
        LCIA samples, with columns = iterations.
        Normally only consisting of one row representing the total score.
        Can also consist of one row per elementary flow for which there is a
        non-null characterization factor.
    """
    LCIA_dir = Path(_get_lcia_dir(result_dir, samples_batch, method))
    arr_fp = LCIA_dir / "{}.npy".format(act_code)
    if not arr_fp.is_file():
        raise ValueError("No file at {}".format(str(arr_fp)))
    return np.load(str(arr_fp))


def load_det_lci(result_dir, act_code):
    """Return precalculated deterministic LCI"""
    result_dir = Path(_check_result_dir(result_dir))
    det_lci_dir = result_dir / "deterministic" / "LCI"
    if not det_lci_dir.is_dir():
        raise ValueError("No LCI arrays at ", str(det_lci_dir))
    det_lci_fp = det_lci_dir / "{}.npy".format(act_code)
    if not det_lci_fp.is_file():
        raise ValueError("No deterministic result for activity with code {}.".format(
            act_code
        ))
    return np.load(str(det_lci_dir))


def load_det_lcia(result_dir, method, act_code, det_lcia_dict=None):
    """Return precalculated deterministic LCIA score"""
    result_dir = Path(_check_result_dir(result_dir))
    method = _check_method(method)
    if not det_lcia_dict:
        det_lcia_dict = _get_det_lcia_dict(result_dir, method)
    if not act_code in det_lcia_dict:
        raise ValueError("No deterministic result for activity with code {} "
                         "in deterministic LCIA dictionary".format(
            act_code
        ))
    return det_lcia_dict[act_code]


def generate_seed_from_pi(i):
    if i>14:
        raise ValueError("Cannot generate seeds this way for i>14")
    i=i+1
    return int(str(math.pi*10**i)[0:i])%2**23


def get_ref_bio_dict_from_common_files(common_files_dirpath):
    # Get reference biosphere dict
    with open(Path(common_files_dirpath) / 'bio_dict.pickle', 'rb') as f:
        ref_bio_dict = pickle.load(f)
    return ref_bio_dict


def _check_lci_missing(result_dir, result_type='probabilistic'):
    """Check if any LCI arrays are missing"""
    with open(result_dir / "common_files" / "ordered_activity_codes.json", "r") as f:
        expected_activity_codes = json.load(f)
    available = sorted([f[0:-4] for f in os.listdir(result_dir / result_type / 'LCI')])
    return sorted(expected_activity_codes) == available
