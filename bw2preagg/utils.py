from pathlib import Path
import math
from brightway2 import *
import presamples
import pickle


def missing_useful_files(result_dir):
    """Return list of missing useful files"""
    useful_files = [
        'ordered_activity_codes.json',  # activity codes
        'deterministic_lci.pickle',  # dict {codes:LCI}
        'product_dict.pickle',  # lca.product_dict
        'bio_dict.pickle',  # lca.biosphere_dict
        'activity_dict.pickle',  # lca.activity_dict
        'tech_params.pickle',  # lca.tech_params
        'bio_params.pickle',  # lca.bio_params
        'IO_Mapping.pickle',  # mapping
        'tech_row_indices.npy',  # PROBABLY NO LONGER NEEDED
        'tech_col_indices.npy',  # PROBABLY NO LONGER NEEDED
        'bio_row_indices.npy',  # PROBABLY NO LONGER NEEDED
        'bio_col_indices.npy'  # PROBABLY NO LONGER NEEDED
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


def _check_result_dir(result_dir):
    """Check that result_dir exists"""
    if not Path(result_dir).is_dir():
        raise ValueError("result_dir {} does not exist".format(result_dir))
    return result_dir


def _get_campaign(sample_batch, expect_base_presamples=False):
    """ Return campaign for given sample_batch"""
    campaign = presamples.Campaign.get_or_none(
        presamples.Campaign.name == "c{}".format(sample_batch)
    )
    if not campaign:
        if expect_base_presamples:
            raise ValueError(
                "No base campaign generated yet, run "
                "generate_base_presample_resource first"
            )
        else:
            campaign = presamples.Campaign.create(name="c{}".format(sample_batch))
            campaign.save()
    return campaign


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
