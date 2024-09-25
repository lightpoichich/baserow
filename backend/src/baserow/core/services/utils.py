from enum import Enum


class ServiceAdhocRefinements(Enum):
    FILTER = "FILTER"
    SORT = "SORT"
    SEARCH = "SEARCH"

    @classmethod
    def to_model_field(cls, refinement: "ServiceAdhocRefinements") -> str:
        value_to_model_field = {
            cls.FILTER: "filterable",
            cls.SORT: "sortable",
            cls.SEARCH: "searchable",
        }
        return value_to_model_field[refinement]
