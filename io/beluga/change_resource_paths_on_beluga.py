from presamples.campaigns import Campaign, PresampleResource
from presamples.utils import validate_presamples_dirpath
from brightway2 import *
from pathlib import Path, PureWindowsPath

if __name__ == "__main__":
    new_path_parent = Path("/home/plesage/scratch/ei36co_balanced_files/preagg_ei36co/presamples/")
    print("IN")
    projects.set_current("ei36co")
    campaigns = Campaign.select()
    for c in campaigns:
        print(c.name)
        for res_path in c:
            resource = PresampleResource.get_or_none(PresampleResource.path==res_path)
            assert resource is not None
            if Path(res_path).parents[0] != new_path_parent:
                print("replacing ", res_path)
                old_path = PureWindowsPath(resource.path)
                resource.path = str(new_path_parent / old_path.name)
                resource.save()
            else:
                print("passing ", res_path)
                pass
    print("half-way, validating")
    for p in new_path_parent.iterdir():
        assert p.parents
        validate_presamples_dirpath(p)
    print("validated")
    c = Campaign.get(Campaign.name == "c0")
    pr = [p for p in c]
    act = Database('ei36co').random()
    print(act)
    mc = MonteCarloLCA({act: 1})
    for _ in range(10):
        next(mc)
    mc1 = MonteCarloLCA({act: 1}, presamples=pr)
    for _ in range(10):
        next(mc1)
    mc2 = MonteCarloLCA({act: 1}, presamples=pr)
    for _ in range(10):
        next(mc2)
    print("MC none")
    print(mc.inventory.sum(axis=1)[0:20])
    print("MC1")
    print(mc1.inventory.sum(axis=1)[0:20])
    print("MC2")
    print(mc2.inventory.sum(axis=1)[0:20])


