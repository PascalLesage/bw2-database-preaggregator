import pytest
from bw2data.tests import bw2test
from brightway2 import *
from shutil import rmtree
import numpy as np

@pytest.fixture(scope="session")
def result_dir(tmpdir_factory):
    mydir = tmpdir_factory.mktemp("result_dir")
    return mydir

@pytest.fixture
@bw2test
def db():
    # Make sure we are starting off with an empty project
    assert not len(Database('db'))
    assert not len(Database('biosphere'))

    biosphere = Database("biosphere")
    biosphere.register()
    biosphere.write({
    ("biosphere", "emission"): {
        'categories': ['water'],
        'name': 'Some emission',
        'type': 'emission',
        'unit': 'kg'
    },
    ("biosphere", "water in"): {
        'categories': ['natural resource'],
        'exchanges': [],
        'name': 'Water in',
        'type': 'natural resource',
        'unit': 'm3'
    },
    ("biosphere", "water out"): {
        'categories': ['water'],
        'exchanges': [],
        'name': 'Water out',
        'type': 'emission',
        'unit': 'm3'
    },
    ("biosphere", "land from"): {
        'categories': ('natural resource', 'land'),
        'exchanges': [],
        'name': 'Transformation, from x',
        'type': 'natural resource',
        'unit': 'm2'
    },
    ("biosphere", "land to"): {
        'categories': ('natural resource', 'land'),
        'exchanges': [],
        'name': 'Transformation, to y',
        'type': 'natural resource',
        'unit': 'm2'
    },
    })
    assert len(Database('biosphere')) == 5

    db = Database("db")
    db.register()
    db.write({
        ("db", "prod_A1"): {
            'type': 'process',
            'name': 'Production A1',
            'unit': 'kg',
            'location': 'GLO',
            'reference product': 'A',
            'production amount': 1,
            'activity type': 'ordinary transforming activity',
            'comment': 'Normal activity, uncertainty lognormal',
            'exchanges': [
                {
                    'name': 'A',
                    'unit': 'kg',
                    'amount': 1.0,
                    'input': ('db', 'prod_A1'),
                    'type': 'production',
                    'uncertainty type': 0,
                },
                {
                    'name': 'B',
                    'unit': 'kg',
                    'amount': 1.2,
                    'input': ('db', 'prod_B'),
                    'type': 'technosphere',
                    'uncertainty type': 2,
                    'loc': np.log(1.2),
                    'scale': 0.1,
                },
                {
                    'name': 'W',
                    'unit': 'kg',
                    'amount': -0.2,
                    'input': ('db', 'market_treat'),
                    'type': 'technosphere',
                    'uncertainty type': 2,
                    'loc': np.log(np.abs(-0.2)),
                    'scale': 0.1,
                    'negative': True
                },
                {
                    'name': 'Some emission',
                    'unit': 'kg',
                    'amount': 1,
                    'input': ('biosphere', 'emission'),
                    'type': 'biosphere',
                    'uncertainty type': 2,
                    'loc': np.log(1),
                    'scale': 0.1,
                },
                {
                    'name': 'water in',
                    'unit': 'cubic meter',
                    'amount': 1,
                    'input': ('biosphere', 'water in'),
                    'type': 'biosphere',
                    'uncertainty type': 2,
                    'loc': np.log(1),
                    'scale': 0.1,
                },
                {
                    'name': 'water out',
                    'unit': 'cubic meter',
                    'amount': 1,
                    'input': ('biosphere', 'water out'),
                    'type': 'biosphere',
                    'uncertainty type': 2,
                    'loc': np.log(1),
                    'scale': 0.1,
                }
            ],
        },
        ("db", "prod_A2"): {
            'type': 'process',
            'name': 'Production A2',
            'unit': 'kg',
            'location': 'GLO',
            'reference product': 'A',
            'production amount': 1,
            'activity type': 'ordinary transforming activity',
            'comment': 'Normal activity, uncertainty triangular',
            'exchanges': [
                {
                    'name': 'A',
                    'unit': 'kg',
                    'amount': 1.0,
                    'input': ('db', 'prod_A2'),
                    'type': 'production',
                    'uncertainty type': 0,
                },
                {
                    'name': 'C',
                    'unit': 'kg',
                    'amount': 1.3,
                    'input': ('db', 'prod_C'),
                    'type': 'technosphere',
                    'uncertainty type': 2,
                    'loc': np.log(0.3),
                    'scale': 0.1,
                },
                {
                    'name': 'W',
                    'unit': 'kg',
                    'amount': -0.3,
                    'input': ('db', 'market_treat'),
                    'type': 'technosphere',
                    'uncertainty type': 5,
                    'loc': -0.2,
                    'minimum': -0.3,
                    'maximum': -0.1,
                },
                {
                    'name': 'Some emission',
                    'unit': 'kg',
                    'amount': 2,
                    'input': ('biosphere', 'emission'),
                    'type': 'biosphere',
                    'uncertainty type': 5,
                    'loc': 2,
                    'minimum': 1,
                    'maximum': 3,
                },
                {
                    'name': 'land from',
                    'unit': 'square meter',
                    'amount': 1,
                    'input': ('biosphere', 'land from'),
                    'type': 'biosphere',
                    'uncertainty type': 5,
                    'loc': 1,
                    'minimum': 0.5,
                    'maximum': 1.5,
                },
                {
                    'name': 'land to',
                    'unit': 'square meter',
                    'amount': 1,
                    'input': ('biosphere', 'land to'),
                    'type': 'biosphere',
                    'uncertainty type': 5,
                    'loc': 1,
                    'minimum': 0.5,
                    'maximum': 1.5,
                },
            ],
        },
        ("db", "market_A"): {
            'type': 'process',
            'name': 'Market for A',
            'unit': 'kg',
            'location': 'GLO',
            'reference product': 'A',
            'production amount': 1,
            'activity type': 'market activity',
            'comment': 'market activity',
            'exchanges': [
                {
                    'name': 'A',
                    'unit': 'kg',
                    'amount': 1.0,
                    'input': ('db', 'market_A'),
                    'type': 'production',
                    'uncertainty type': 0,
                },
                {
                    'name': 'A',
                    'unit': 'kg',
                    'amount': 0.5,
                    'input': ('db', 'prod_A1'),
                    'type': 'technosphere',
                    'uncertainty type': 2,
                    'loc': np.log(0.5),
                    'scale': 0.1
                },
                {
                    'name': 'A',  # input from prod_A2
                    'unit': 'kg',
                    'amount': 0.5,
                    'input': ('db', 'prod_A2'),
                    'type': 'technosphere',
                    'uncertainty type': 2,
                    'loc': np.log(0.5),
                    'scale': 0.1
                },
                {
                    'name': 'A',  # input from self, to compensate losses
                    'unit': 'kg',
                    'amount': 0.1,
                    'input': ('db', 'market_A'),
                    'type': 'technosphere',
                    'uncertainty type': 2,
                    'loc': np.log(0.1),
                    'scale': 0.1
                },
                {
                    'name': 'W',  # losses
                    'unit': 'kg',
                    'amount': -0.1,
                    'input': ('db', 'market_treat'),
                    'type': 'technosphere',
                    'uncertainty type': 2,
                    'loc': np.log(0.1),
                    'scale': 0.1,
                    'negative': True
                },
            ],
        },
        ("db", "prod_B"): {
            'type': 'process',
            'name': 'Production B',
            'unit': 'kg',
            'location': 'GLO',
            'reference product': 'B',
            'production amount': 1,
            'activity type': 'ordinary transforming activity',
            'comment': 'Normal activity, uncertainty lognormal',
            'exchanges': [
                {
                    'name': 'B',
                    'unit': 'kg',
                    'amount': 1.0,
                    'input': ('db', 'prod_B'),
                    'type': 'production',
                    'uncertainty type': 0,
                },
                {
                    'name': 'A',
                    'unit': 'kg',
                    'amount': 0.1,
                    'input': ('db', 'market_A'),
                    'type': 'technosphere',
                    'uncertainty type': 2,
                    'loc': np.log(0.1),
                    'scale': 0.1,
                },
                {
                    'name': 'W',
                    'unit': 'kg',
                    'amount': -0.1,
                    'input': ('db', 'market_treat'),
                    'type': 'technosphere',
                    'uncertainty type': 2,
                    'loc': np.log(np.abs(-0.1)),
                    'scale': 0.1,
                    'negative': True
                },
                {
                    'name': 'Some emission',
                    'unit': 'kg',
                    'amount': 5,
                    'input': ('biosphere', 'emission'),
                    'type': 'biosphere',
                    'uncertainty type': 2,
                    'loc': np.log(5),
                    'scale': 0.1,
                },
            ],
        },
        ("db", "prod_C"): {
            'type': 'process',
            'name': 'Production C',
            'unit': 'kg',
            'location': 'GLO',
            'reference product': 'C',
            'production amount': 1,
            'activity type': 'ordinary transforming activity',
            'comment': 'Normal activity, uncertainty lognormal',
            'exchanges': [
                {
                    'name': 'C',
                    'unit': 'kg',
                    'amount': 1.0,
                    'input': ('db', 'prod_C'),
                    'type': 'production',
                    'uncertainty type': 0,
                },
                {
                    'name': 'A',
                    'unit': 'kg',
                    'amount': 0.2,
                    'input': ('db', 'market_A'),
                    'type': 'technosphere',
                    'uncertainty type': 2,
                    'loc': np.log(0.2),
                    'scale': 0.1,
                },
                {
                    'name': 'W',
                    'unit': 'kg',
                    'amount': -0.2,
                    'input': ('db', 'market_treat'),
                    'type': 'technosphere',
                    'uncertainty type': 2,
                    'loc': np.log(np.abs(-0.2)),
                    'scale': 0.1,
                    'negative': True
                },
                {
                    'name': 'Some emission',
                    'unit': 'kg',
                    'amount': 10,
                    'input': ('biosphere', 'emission'),
                    'type': 'biosphere',
                    'uncertainty type': 2,
                    'loc': np.log(10),
                    'scale': 0.1,
                },
            ],
        },
        ("db", "treat_1"): {
            'type': 'process',
            'name': 'Treatment 1',
            'unit': 'kg',
            'location': 'GLO',
            'reference product': 'W',
            'production amount': -1,
            'activity type': 'ordinary transforming activity',
            'comment': 'Normal treatment activity, uncertainty lognormal',
            'exchanges': [
                {
                    'name': 'W',
                    'unit': 'kg',
                    'amount': -1.0,
                    'input': ('db', 'treat_1'),
                    'type': 'production',
                    'uncertainty type': 0,
                },
                {
                    'name': 'Some emission',
                    'unit': 'kg',
                    'amount': 2,
                    'input': ('biosphere', 'emission'),
                    'type': 'biosphere',
                    'uncertainty type': 2,
                    'loc': np.log(2),
                    'scale': 0.1,
                },
            ],
        },
        ("db", "treat_2"): {
            'type': 'process',
            'name': 'Treatment 2',
            'unit': 'kg',
            'location': 'GLO',
            'reference product': 'W',
            'production amount': -1,
            'comment': 'Normal treatment activity, uncertainty lognormal',
            'activity type': 'ordinary transforming activity',
            'exchanges': [
                {
                    'name': 'W',
                    'unit': 'kg',
                    'amount': -1.0,
                    'input': ('db', 'treat_2'),
                    'type': 'production',
                    'uncertainty type': 0,
                },
                {
                    'name': 'Some emission',
                    'unit': 'kg',
                    'amount': 10,
                    'input': ('biosphere', 'emission'),
                    'type': 'biosphere',
                    'uncertainty type': 2,
                    'loc': np.log(10),
                    'scale': 0.1,
                },
            ],
        },
        ("db", "market_treat"): {
            'type': 'process',
            'name': 'Treatment market',
            'unit': 'kg',
            'location': 'GLO',
            'reference product': 'W',
            'production amount': -1,
            'activity type': 'market activity',
            'comment': 'treatment market, uncertainty lognormal',
            'exchanges': [
                {
                    'name': 'W',
                    'unit': 'kg',
                    'amount': -1.0,
                    'input': ('db', 'market_treat'),
                    'type': 'production',
                    'uncertainty type': 0,
                },
                {
                    'name': 'W',
                    'unit': 'kg',
                    'amount': -0.5,
                    'input': ('db', 'treat_1'),
                    'type': 'technosphere',
                    'uncertainty type': 2,
                    'scale': 0.1,
                    'loc': np.log(1),
                    'negative': True
                },
                {
                    'name': 'W',
                    'unit': 'kg',
                    'amount': -0.5,
                    'input': ('db', 'treat_2'),
                    'type': 'technosphere',
                    'uncertainty type': 2,
                    'scale': 0.1,
                    'loc': np.log(1),
                    'negative': True
                },
            ],
        },
    })
    yield {'project': projects.current}

    rmtree(projects.dir, ignore_errors=True)
