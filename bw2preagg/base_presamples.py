from pathlib import Path
from brightway2 import *
import presamples
from stats_arrays import MCRandomNumberGenerator
from bw2data.utils import TYPE_DICTIONARY
import numpy as np
from bw2preagg.utils import _check_project, _check_database,  _check_result_dir, \
    _get_campaign, generate_seed_from_pi


def generate_base_presamples(project_name, database_name, result_dir, iterations,
                             samples_batch, overwrite_ps=True, ps_base_name="base"):
    """Generate presamples for all elements of A and B matrices of given database

    The presamples are stored in a presamples resource in result_dir and added
    to a presamples campaign for easy reuse.
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
    ps_name_base : str, default="base"
        Base name for presamples resource.

    Returns
    -------
    None
    """
    projects.set_current(_check_project(project_name))
    db = Database(_check_database(database_name))
    result_dir = Path(_check_result_dir(result_dir))
    if samples_batch > 14:
        raise ValueError("Cannot use samples_batch value greater than 14")
    sacrificial_LCA = LCA({act:act.get('production amount', 1) for act in db})
    sacrificial_LCA.lci()
    seed = generate_seed_from_pi(samples_batch)
    print("Generating technosphere matrix samples")
    tech_samples, tech_indices = indices_and_samples_from_params(
        sacrificial_LCA.tech_params, iterations=iterations,
        seed=seed
    )
    print("Generating biosphere matrix samples")
    bio_samples, bio_indices = indices_and_samples_from_params(
        sacrificial_LCA.bio_params, iterations=iterations,
        seed=seed
    )
    print("Storing presamples")
    ps_dir = result_dir/"presamples"
    ps_dir.mkdir(exist_ok=True)
    ress_id = "{}_{}".format(ps_base_name, samples_batch)

    ps_id, ps_path = presamples.create_presamples_package(
        matrix_data=[
            (tech_samples, tech_indices, 'technosphere'),
            (bio_samples, bio_indices, 'biosphere')
        ],
        name=ress_id, id_=ress_id, overwrite=overwrite_ps,
        dirpath=ps_dir, seed='sequential'
    )
    ps_ress, _ = presamples.PresampleResource.get_or_create(
        name=ress_id,
        path=ps_path
    )
    campaign = _get_campaign(samples_batch)
    if not ps_ress in list(campaign.packages):
        campaign.add_presample_resource(ps_ress)

def indices_and_samples_from_params(params, iterations, seed=None):
    """Format heterogeneous parameter array for presamples"""
    rev_mapping = {v:k for k, v in mapping.items()}
    input_keys_unformated = np.vectorize(rev_mapping.get)(params['input'])
    output_keys_unformated = np.vectorize(rev_mapping.get)(params['output'])
    rev_TYPE_DICTIONARY = {v: k for k, v in TYPE_DICTIONARY.items()}
    type_array = np.vectorize(rev_TYPE_DICTIONARY.get)(params['type'])
    indices = [
        ((input_key, input_code), (output_key, output_code), exc_type)
        for input_key, input_code, output_key, output_code, exc_type in zip(
            input_keys_unformated[0], input_keys_unformated[1],
            output_keys_unformated[0], output_keys_unformated[1],
            type_array
        )
            ]
    samples = np.empty(shape=(params.shape[0], iterations))
    rng = MCRandomNumberGenerator(params, seed)
    for i in range(iterations):
        samples[:, i] = next(rng)
    return samples, indices
