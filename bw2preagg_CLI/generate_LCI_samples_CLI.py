import click
from bw2preagg.generate_LCI_samples import dispatch_lci_calculators

@click.command()
@click.option('--project_name', default='default', help='Brightway2 project name', type=str)
@click.option('--database_name', help='Database name', type=str)
@click.option('--result_dir', help='Base directory path for precalculated samples', type=str)
@click.option('--samples_batch', help='Integer representing the presample package', type=int, default=None)
@click.option('--parallel_jobs', help='Number of CPUs allocated to this work', type=int)
@click.option('--slice_id', help='Slice ID for job arrays, useful when dispatching calculations on computer clusters', type=int, default=None)
@click.option('--number_of_slices', help='Total number of slices for job arrays, useful when dispatching calculations on computer clusters', type=int, default=None)
def dispatch_lci_calculators_CLI(project_name, database_name, result_dir, samples_batch,
                             parallel_jobs, slice_id=None, number_of_slices=None):
    """CLI-friendly access to bw2preagg.dispatch_lci_calculators, to generate LCI samples"""
    dispatch_lci_calculators(project_name, database_name, result_dir, samples_batch,
                             parallel_jobs, slice_id, number_of_slices)

if __name__=='__main__':
    __spec__ = None
    dispatch_lci_calculators_CLI()