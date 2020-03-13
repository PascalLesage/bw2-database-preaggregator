""" Initial setup of the brightway2 project.

Creates project, imports databases and generates some useful data.
Should be run first.
"""
import click
from bw2preagg.setup_project import setup_project
import time

@click.command()
@click.option('--project_name', default='default', help='Brightway2 project name', type=str)
@click.option('--database_name', help='Database name', type=str)
@click.option('--database_dir', help='Directory with ecoSpold files for importing LCI data', type=str)
@click.option('--result_dir', help='Base directory path for results', type=str)
@click.option('--overwrite_project', help='First delete project if it exists', type=bool, default=False)
@click.option('--overwrite_database', help='First delete database if it exists', type=bool, default=False)
@click.option('--force_write_common_files', help='Write series of database-related files to result_dir', type=bool, default=True)
def setup_project_CLI(project_name, database_dir, database_name, result_dir,
                      overwrite_project, overwrite_database, force_write_common_files):
    """ CLI-friendly access to bw2preagg.setup_project to create project and import databases, generate common files"""
    t0 = time.time()
    setup_project(project_name, database_dir, database_name, result_dir,
                  overwrite_project, overwrite_database, force_write_common_files)
    print("Executed in {} seconds".format(time.time()-t0))

if __name__ == '__main__':
    __spec__ = None
    setup_project_CLI()
