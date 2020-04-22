README
--------

bw2preagg is used to generate dependently sampled LCI and LCIA arrays for whole databases.

It uses [Brightway2](http://brightway.dev/) framework and [presamples](https://presamples.readthedocs.io/en/latest/). 
The arrays are stored as numpy.ndarray files, and can be integrated in Brightway2 models using other modules ([brightway2-aggregated](https://github.com/CIRAIG/brightway2-aggregated), [presamples]((https://presamples.readthedocs.io/en/latest/))).

The resulting result arrays allow the use of aggregated LCI or LCIA results (also known as cradle-to-gate results) in LCA while also correctly integrating the uncertainty of LCI data, see [Lesage et al. 2018](https://doi.org/10.1007/s11367-018-1444-x).

Generating samples of cradle-to-gate results for all activities in a database can be a lengthy process, especially when dealing with large LCI databases like ecoinvent. 
The functions are therefore geared towards large, bulk calculations, by e.g. facilitating multiprocessing and breaking down the task in multiple “batches” that can run on different systems.

For more information, consult the [documentation](https://bw2preagg.readthedocs.io/en/latest/). 