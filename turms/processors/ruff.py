import os
import sys
import sysconfig
import tempfile
import subprocess

from pydantic import Field
from turms.processors.base import Processor, ProcessorConfig
from turms.config import GeneratorConfig


def find_ruff_bin() -> str:
    """Return the ruff binary path."""

    ruff_exe = "ruff" + sysconfig.get_config_var("EXE")

    scripts_path = os.path.join(sysconfig.get_path("scripts"), ruff_exe)
    if os.path.isfile(scripts_path):
        return scripts_path

    if sys.version_info >= (3, 10):
        user_scheme = sysconfig.get_preferred_scheme("user")
    elif os.name == "nt":
        user_scheme = "nt_user"
    elif sys.platform == "darwin" and sys._framework:
        user_scheme = "osx_framework_user"
    else:
        user_scheme = "posix_user"

    user_path = os.path.join(
        sysconfig.get_path("scripts", scheme=user_scheme), ruff_exe
    )
    if os.path.isfile(user_path):
        return user_path

    # Search in `bin` adjacent to package root (as created by `pip install --target`).
    pkg_root = os.path.dirname(os.path.dirname(__file__))
    target_path = os.path.join(pkg_root, "bin", ruff_exe)
    if os.path.isfile(target_path):
        return target_path

    raise FileNotFoundError(scripts_path)


class RuffProcessorConfig(ProcessorConfig):
    type: str = "turms.processors.ruff.RuffProcessor"


class RuffProcessor(Processor):
    config: RuffProcessorConfig = Field(default_factory=RuffProcessorConfig)

    def run(self, gen_file: str, config: GeneratorConfig):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
            tmp.write(gen_file)

        ruff = os.fsdecode(find_ruff_bin())
        completed_process = subprocess.run([ruff, "format", tmp.name])

        with open(tmp.name, "r") as tmp:
            out = tmp.read()
            os.unlink(tmp.name)
            return out
