from abc import abstractmethod

from pydantic import BaseModel
from pydantic_settings import BaseSettings
from turms.config import GeneratorConfig


class ProcessorConfig(BaseSettings):
    type: str

    class Config:
        extra = "forbid"
        arbitrary_types_allowed = True

class Processor(BaseModel):
    """Base class for all processors

    Processors are used to modify the generated python code before it is written to the file.
    You can use processors to enforce specific styles on the generated python code like (black
    or isort) or to add additional code to the generated python code.
    """

    config: ProcessorConfig

    class Config:
        arbitrary_types_allowed = True

    @abstractmethod
    def run(gen_file: str, config: GeneratorConfig):
        ...  # pragma: no cover
