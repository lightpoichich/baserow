import abc
from typing import List, Dict, Any

from baserow.core.registry import (
    Instance,
    Registry,
)


class RowMetadataType(Instance, abc.ABC):
    """"""

    @abc.abstractmethod
    def generate_metadata_for(self, table, row_ids: List[int]) -> Dict[int, Any]:
        pass


class RowMetadataRegistry(Registry):
    """"""

    name = "row_metadata"


row_metadata_registry = RowMetadataRegistry()
