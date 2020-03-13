""" Initial setup of the brightway2 project.

Creates project, imports databases and generates some useful data.
Should be run first.
"""
from pathlib import Path
import pickle
import json
import numpy as np
from brightway2 import *
from .utils import missing_useful_files


def setup_project(project_name, database_dir, database_name, result_dir,
                  overwrite_project, overwrite_database, force_write_common_files,
                  default_bw2setup):
    """ Create project and import databases, generate common files

    Parameters
    -----------
    project_name : str
        Name of the brightway2 project in which to import data
    database_name : str
        Name to give the LCI database
    database_dir : str
        Path to directory with ecoSpold2 data to be imported, None if LCI
        database not to be imported
    result_dir : str
        Path to directory where data used by bw2preagg is saved (so-called
        common_files), None if such data should not be generated
    overwrite_project : bool, default=False
        If True, then the project is deleted first, and all data is reimported
        for a clean slate import
    overwrite_database : bool, default=False
        If True, then the LCI database is deleted first, and LCI data is
        reimported
    force_write_common_files : bool, default=True
        If True, then the common files are generated even if they already exist
        at given location
    default_bw2setup: bool, default=True
        If True, run bw2setup to include default elementary flows and LCIA methods

    Returns
    -------
    None
    """
    # Delete project on demand
    if overwrite_project and project_name in projects:
        print("Deleting preexisting project")
        projects.delete_project(project_name, delete_dir=True)
    # Create new project or switch to existing project
    projects.set_current(project_name)
    # Setup new project, if necessary
    if default_bw2setup:
        bw2setup()
    # Import LCI database, if necessary
    if not overwrite_database and database_name in databases:
        print("Importing of {} not necessary".format(database_name))
        pass
    else:
        importer = _prepare_import(database_dir, database_name)
        print("Importing {}".format(database_name))
        if database_name in databases and overwrite_database:
            print("Deleting {}".format(database_name))
            Database(database_name).delete()
            Database(database_name).deregister()
        importer.write_database()

    # Generate common data
    if missing_useful_files(result_dir) or force_write_common_files:
        _generate_common_files(result_dir, database_name)
    else:
        print("No common files to generate")


def _prepare_import(database_dir, database_name):
    """Check ecoSpolds can be imported

    Returns SingleOutputEcospold2Importer with strategies applied it is possible
    to write the data
    Will raise an error if something prevents it.
    """
    if not database_name:
        raise ValueError(
            "Cannot overwrite LCI database without database_name"
        )
    if not Path(database_dir).is_dir():
        raise ValueError(
            "database_dir does not exist, cannot import LCI data"
        )

    db_importer = SingleOutputEcospold2Importer(database_dir, database_name)
    db_importer.apply_strategies()
    if not db_importer.statistics()[2] == 0:
        raise ValueError(
            "{} unlinked exchanges when trying to import database".format(
                db_importer.statistics()[2]
            )
        )
    return db_importer


def _generate_common_files(result_dir, database_name):
    """Generate and save common files used in subsequent steps"""
    print("Generating common files")
    common_files_dir = Path(result_dir)/'common_files'
    common_files_dir.mkdir(exist_ok=True, parents=True)

    # Activity codes
    db = Database(database_name)
    activity_codes = [act.key[1] for act in db]
    activity_codes.sort()
    with open(common_files_dir/'ordered_activity_codes.json', "w") as f:
        json.dump(activity_codes, f, indent=4)

    # Generate sacrificial LCA whose attributes will be saved
    collector_functional_unit = {act:act.get('production amount', 1) for act in db}
    sacrificial_lca = LCA(collector_functional_unit)
    sacrificial_lca.lci()

    # Save various attributes for eventual reuse in interpretation
    # LCA dicts, used to identify matrix coordinates
    with open(common_files_dir/'product_dict.pickle', "wb") as f:
        pickle.dump(sacrificial_lca.product_dict, f)
    with open(common_files_dir/'bio_dict.pickle', "wb") as f:
        pickle.dump(sacrificial_lca.biosphere_dict, f)
    with open(common_files_dir/'activity_dict.pickle', "wb") as f:
        pickle.dump(sacrificial_lca.activity_dict, f)

    # LCA parameter arrays
    with open(common_files_dir/'tech_params.pickle', "wb") as f:
        pickle.dump(sacrificial_lca.tech_params, f)
    with open(common_files_dir/'bio_params.pickle', "wb") as f:
        pickle.dump(sacrificial_lca.bio_params, f)

    # Mapping
    with open(common_files_dir/'IO_Mapping.pickle', "wb") as f:
        pickle.dump({v: k for k, v in mapping.items()}, f)

    # Indices
    np.save(
        common_files_dir/'tech_row_indices',
        sacrificial_lca.technosphere_matrix.tocoo().row
    )
    np.save(
        common_files_dir/'tech_col_indices',
        sacrificial_lca.technosphere_matrix.tocoo().col
    )
    np.save(
        common_files_dir/'bio_row_indices',
        sacrificial_lca.biosphere_matrix.tocoo().row
    )
    np.save(
        common_files_dir/'bio_col_indices',
        sacrificial_lca.biosphere_matrix.tocoo().col
    )

    # Deterministic LCI results
    print("Generating deterministic LCA results")
    lci_dict = {}
    for code in activity_codes:
        try:
            act = get_activity((database_name, code))
            sacrificial_lca.redo_lci({act: act.get('production amount', 1)})
            lci_dict[code] = sacrificial_lca.inventory.sum(axis=1)
        except Exception as err:
            print("******************")
            print(err)
            print("******************")
            lci_dict[code] = "Missing"
    with open(common_files_dir/'deterministic_lci.pickle', "wb") as f:
        pickle.dump(lci_dict, f)
