from abc import ABC, abstractmethod

__all__ = ['Rotable']


class Rotable(ABC):
    """ Rotable interface """

    @property
    @abstractmethod
    def direction(self) -> int:
        """

        :return:
        """
        ...

    @direction.setter
    @abstractmethod
    def direction(self, direction: int) -> None:
        """

        :param direction:
        :return:
        """
        ...

    @property
    @abstractmethod
    def directions_number(self) -> int:
        """

        :return:
        """
        ...

    @property
    @abstractmethod
    def angular_velocity(self) -> int:
        """

        :return:
        """
        ...


# class RotableObject(Rotable):
#     def __init__(self, o: UObject):
#         self._o = o
#
#     def get_direction(self) -> int:
#         return self._o.get_property('direction')
#
#     def set_direction(self, direction: int) -> None:
#         self._o.set_property('direction', direction)
#
#     def get_direction_number(self) -> int:
#         return self._o.get_property('directions_number')
#
#     def get_angular_velocity(self) -> int:
#         return self._o.get_property('angular_velocity')
