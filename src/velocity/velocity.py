from statistics import mean
from functools import reduce


class VelocityItem:
    def __init__(
        self, sprint_name, committed_sp, compleated_sp, capacity: float
    ) -> None:
        self.__sprint_name = sprint_name
        self.__committed_sp = committed_sp
        self.__compleated_sp = compleated_sp
        if capacity >= 0 and capacity <= 1:
            self.__capacity = capacity
        else:
            raise ValueError(
                f"Invalid valuse: {capacity}. The value should be between 0 and 1."
            )

    @property
    def sprint_name(self) -> str:
        return self.__sprint_name

    @property
    def committed_sp(self) -> int:
        return self.__committed_sp

    @property
    def compleated_sp(self) -> int:
        return self.__compleated_sp

    @property
    def capacity(self) -> int:
        return self.__capacity

    @property
    def velocity(self) -> int:
        return round(self.compleated_sp * self.capacity, 0)


class Velocity:
    def __init__(self, data: list[VelocityItem]) -> None:
        self.__data = data

    def calculate_velocity(self) -> float:
        def _get_velocity(data: list[VelocityItem]) -> list[int]:
            fun_get_velocity = lambda d: d.velocity
            return list(map(fun_get_velocity, data))

        return mean(_get_velocity(self.__data))
