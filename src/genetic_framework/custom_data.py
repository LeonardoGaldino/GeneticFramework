from typing import Dict
from abc import ABC


class CustomDataHolder(ABC):
    """Class that defines custom_data: data that some subclasses need to have
    in its class object, not in an instance.
    """
    custom_data: Dict = {}

    @classmethod
    def set_custom_data(cls, custom_data: Dict) -> None:
        cls.custom_data = custom_data

