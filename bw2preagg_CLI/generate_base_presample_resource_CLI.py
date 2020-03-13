import click
import time
from bw2preagg.generate_base_presample_resource import generate_base_presamples

@click.command()
@click.option('--project_name', default='default', help='Brightway2 project name', type=str)
@click.option('--database_name', help='Database name', type=str)
@click.option('--result_dir', help='Base directory path for results', type=str)
@click.option('--iterations', help='Number of iterations in sample batch', type=int)
@click.option('--sample_batch', help='Sequential integer id for sample batch', type=int)
@click.option('--overwrite_ps', help='Overwrite presamples package if exists', default=True, type=bool)
@click.option('--ps_base_name', help='Base name for presamples names and ids', default="base", type=str)
def generate_base_presamples_CLI(project_name, database_name, result_dir, iterations,
                             sample_batch, overwrite_ps=True, ps_base_name="base"):
    """CLI-friendly access to bw2preagg.generate_base_presamples, to generate presamples for
    all elements of A and B matrices of given db
    """
    t0 = time.time()
    generate_base_presamples(project_name, database_name, result_dir, iterations,
                             sample_batch, overwrite_ps, ps_base_name)
    print("Executed in {} seconds".format(time.time() - t0))

if __name__ == '__main__':
    __spec__ = None
    generate_base_presamples_CLI()