import pytest
from brightway2 import *
from presamples import Campaign, PresampleResource, PresamplesPackage, PackagesDataLoader
from bw2preagg.setup_project import setup_project, _generate_common_files, \
    missing_useful_files
from bw2preagg import utils
from bw2preagg.generate_base_presample_resource import generate_base_presamples
import os
from pathlib import Path
import numpy as np

def test_write_matrices(db):
    """ pytest resources written as expected"""
    assert len(Database("db")) == 8
    assert len(Database("biosphere")) == 5


def test_setup_project(db, result_dir):
    """ Useful files written"""
    result_dir = Path(result_dir)
    common_files_dir = result_dir / 'common_files'
    if common_files_dir.is_dir():
        assert len(os.listdir(common_files_dir)) == 0
    setup_project(
        project_name=db['project'], database_dir=None, database_name='db',
        result_dir=result_dir, overwrite_project=False,
        overwrite_database=False, force_write_common_files=False,
        default_bw2setup=False
    )
    assert common_files_dir.is_dir()
    assert len(os.listdir(common_files_dir)) > 0
    ordered_activity_codes_path = common_files_dir / "ordered_activity_codes.json"
    assert ordered_activity_codes_path.is_file()
    assert not missing_useful_files(result_dir)
    os.remove(common_files_dir/'product_dict.pickle') # Randomly remove one file
    assert missing_useful_files(result_dir) == ['product_dict.pickle']

def test_utils(db):
    with pytest.raises(ValueError, match="Project boom does not exist, run setup_project first"):
        utils._check_project("boom")
    with pytest.raises(ValueError, match="Database boom has not been set up, run setup_project first"):
        utils._check_database("boom")
    Database('boom').register()
    with pytest.raises(ValueError, match="Database boom is empty, run setup_project with overwrite_database=True"):
        utils._check_database("boom")
    with pytest.raises(ValueError, match="result_dir boom does not exist"):
        utils._check_result_dir("boom")

def test_seed():
    assert utils.generate_seed_from_pi(0) == 3%2**23
    assert utils.generate_seed_from_pi(1) == 31%2**23
    assert utils.generate_seed_from_pi(2) == 314%2**23
    assert utils.generate_seed_from_pi(3) == 3141%2**23
    assert utils.generate_seed_from_pi(4) == 31415%2**23
    assert utils.generate_seed_from_pi(5) == 314159%2**23
    assert utils.generate_seed_from_pi(6) == 3141592%2**23
    assert utils.generate_seed_from_pi(7) == 31415926%2**23
    assert utils.generate_seed_from_pi(8) == 314159265%2**23
    assert utils.generate_seed_from_pi(9) == 3141592653%2**23
    assert utils.generate_seed_from_pi(10) == 31415926535%2**23
    assert utils.generate_seed_from_pi(11) == 314159265358%2**23
    assert utils.generate_seed_from_pi(12) == 3141592653589%2**23
    assert utils.generate_seed_from_pi(13) == 31415926535897%2**23
    assert utils.generate_seed_from_pi(14) == 314159265358979%2**23
    with pytest.raises(ValueError, match="Cannot generate seeds this way for i>14"):
        utils.generate_seed_from_pi(15)

def test_get_ref_bio_dict_from_common_files(result_dir):
    bio_dict = utils.get_ref_bio_dict_from_common_files(Path(result_dir)/'common_files')
    expected = {
        ('biosphere', 'emission'): 0,
        ('biosphere', 'water in'): 1,
        ('biosphere', 'water out'): 2,
        ('biosphere', 'land from'): 3,
        ('biosphere', 'land to'): 4
    }
    assert bio_dict == expected

def test_get_campaign():
    pass

def test_generate_base_presamples(db, result_dir):
    assert len(Campaign.select()) == 0
    generate_base_presamples(
        project_name='default',
        database_name='db',
        result_dir=result_dir,
        iterations=10,
        sample_batch=0,
        overwrite_ps=True,
        ps_base_name="base"
    )
    assert len(Campaign.select()) == 1
    c = utils._get_campaign(0)
    assert len(c) == 1
    pr = PresampleResource.get(PresampleResource.name == 'base_0')
    pr_path = [p for p in c][0]
    assert pr.path == pr_path
    pdl = PackagesDataLoader([pr_path])
    print(pdl.parameter_data_loaded)

    """
    assert pp.seed == 'sequential'
    assert pp.ncols == 10
    techno_resources = [ress for ress in pp.resources if ress['type']=='technosphere']
    assert len(techno_resources) == 1
    techno_resource = techno_resources[0]
    techno_indices = np.load(pp.path/techno_resource['indices']['filepath'])
    print(techno_indices)
    bio_resource = [ress for ress in pp.resources if ress['type']=='biosphere']
    assert len(bio_resource) == 1
    """



