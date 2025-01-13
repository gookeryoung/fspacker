import yaml
from config import CWD
from modules.module_b import function_b


def function_a():
    ast = CWD / "assets"
    cfg = ast / "config.yml"

    with open(cfg, "r") as f:
        config_dict = yaml.safe_load(f)

    print(f"{config_dict=}")
    print(f"{config_dict.get('names')=}")
    function_b()
