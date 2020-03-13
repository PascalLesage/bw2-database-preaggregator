import click
import time
from bw2preagg.generate_balancing_presample_resources import generate_balancing_presamples

@click.command()
@click.option('--project_name', default='default', help='Brightway2 project name', type=str)
@click.option('--database_name', help='Database name', type=str)
@click.option('--result_dir', help='Base directory path for results', type=str)
@click.option('--iterations', help='Number of iterations in sample batch', type=int)
@click.option('--sample_batch', help='Sequential integer id for sample batch', type=int)
@click.option('--overwrite_ps', help='Overwrite presamples package if exists', default=True, type=bool)
@click.option('--balance_water', help='Balance water exchanges', default=True, type=bool)
@click.option('--balance_land', help='Balance land transformation exchanges', default=True, type=bool)
@click.option('--ecoinvent_version', help='ecoinvent release number, used by water exchange balancer', default='3.6', type=str)
@click.option('--expect_base_presamples', help='Raise error if base presamples do not exist', default=True, type=bool)
@click.option('--land_from_patterns', help='List of string patterns identifying land states prior to transformation', default=['Transformation, from'], type=list)
@click.option('--land_to_patterns', help='List of string patterns identifying land states after transformation', default=['Transformation, to'], type=list)
def generate_balancing_presamples_CLI(
        project_name, database_name, result_dir, iterations, sample_batch,
        overwrite_ps=True, balance_water=True, balance_land=True,
        ecoinvent_version="3.6", land_from_patterns=['Transformation, from'],
        land_to_patterns=['Transformation, to'], expect_base_presamples=True):
    """CLI-friendly access to bw2preagg.generate_balancing_presamples, to generate balancing presamples for a given db"""
    t0 = time.time()
    generate_balancing_presamples(project_name, database_name, result_dir, iterations, sample_batch,
        overwrite_ps, balance_water, balance_land, ecoinvent_version, land_from_patterns,
        land_to_patterns, expect_base_presamples)
    print("Executed in {} seconds".format(time.time() - t0))


if __name__ == '__main__':
    __spec__ = None
    generate_balancing_presamples_CLI()