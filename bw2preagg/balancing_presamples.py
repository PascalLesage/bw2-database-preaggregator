from pathlib import Path
import numpy as np
from brightway2 import *
import presamples
from bw2waterbalancer import DatabaseWaterBalancer
from bw2landbalancer import DatabaseLandBalancer
from bw2preagg.utils import _check_project, _check_database,  _check_result_dir, \
    _get_campaign, generate_seed_from_pi


def generate_balancing_presamples(
        project_name, database_name, result_dir, iterations, samples_batch,
        overwrite_ps=True, balance_water=True, balance_land=True,
        ecoinvent_version="3.6", land_from_patterns=['Transformation, from'],
        land_to_patterns=['Transformation, to'], expect_base_presamples=True):
    """Generate balancing presamples for a given db

    These can be sampled for water exchanges and/or land transformation
    exchanges. The presamples are stored in a presamples resource in result_dir
    and added to a presamples campaign for easy reuse.
    It is recommended that presamples are generated in batches (e.g. of 1000
    iterations each). This is implemented via the samples_batch argument.

    Parameters
    -----------
    project_name : str
        Name of the brightway2 project where the database is imported
    database_name : str
        Name of the LCI database
    result_dir : str
        Path to directory where results are stored
    iterations : int
        Number of iterations to include in sample
    samples_batch : int, default=0
        Integer id for sample batch. Used for campaigns names and for
        generating a seed for the RNG. The maximum value is 14.
    overwrite_ps : bool, default=True
        Overwrite presamples package if it exists
    balance_water : bool, default=True
        Balance water exchanges
    balance_land : bool, default=True
        Balance land transformation exchanges
    ecoinvent_version : str, default="3.6"
        Release number of ecoinvent database
    land_from_patterns : list of string, default=['Transformation, from']
        Patterns used to identify land transformation inputs
    land_to_patterns : list of string, default=['Transformation, to']
        Patterns used to identify land transformation outputs
    expect_base_presamples : bool, default=True
        If True, ValueError is raised if base presamples package for
        corresponding samples_batch is missing

    Returns
    -------
    None
    """
    projects.set_current(_check_project(project_name))
    db = Database(_check_database(database_name))
    result_dir = Path(_check_result_dir(result_dir))
    campaign = _get_campaign(samples_batch, expect_base_presamples)
    seed = generate_seed_from_pi(samples_batch)
    ps_dir = result_dir / "presamples"

    if balance_water:
        print("Generating water balancing samples")
        np.random.seed(seed)
        water_ress_id = "water_{}".format(samples_batch)
        water_balancer = DatabaseWaterBalancer(
            ecoinvent_version=ecoinvent_version, database_name=database_name
        )
        water_balancer.add_samples_for_all_acts(iterations)
        water_ps_id, water_ps_path = water_balancer.create_presamples(
            name=water_ress_id, id_=water_ress_id, overwrite=overwrite_ps,
            dirpath=ps_dir, seed='sequential')
        water_ps_ress, _ = presamples.PresampleResource.get_or_create(
            name=water_ress_id,
            path=water_ps_path
        )
        if not water_ps_ress in list(campaign.packages):
            campaign.add_presample_resource(water_ps_ress)

    if balance_land:
        print("Generating land transformation balancing samples")
        np.random.seed(seed)
        land_ress_id = "land_{}".format(samples_batch)
        land_balancer = DatabaseLandBalancer(
            database_name=database_name,
            land_from_patterns=land_from_patterns,
            land_to_patterns=land_to_patterns,
            )
        land_balancer.add_samples_for_all_acts(iterations)
        land_ps_id, land_ps_path = land_balancer.create_presamples(
            name=land_ress_id, id_=land_ress_id, overwrite=overwrite_ps,
            dirpath=ps_dir, seed='sequential')
        land_ps_ress, _ = presamples.PresampleResource.get_or_create(
            name=land_ress_id,
            path=land_ps_path
        )
        if not land_ps_ress in list(campaign.packages):
            campaign.add_presample_resource(land_ps_ress)
