import yaml
from config import CWD
from modules.module_b import function_b


def function_a():
    ast = CWD / "assets"
    cfg = ast / "config.yml"

    config_dict = yaml.load(cfg, yaml.FullLoader)
    print(f"{config_dict=}")

    function_b()
