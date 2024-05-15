import pathlib
import tomli

path = pathlib.Path(__file__).parent / "param.toml"
with path.open(mode="rb") as fp:
    param = tomli.load(fp)
