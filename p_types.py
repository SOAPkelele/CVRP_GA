from dataclasses import dataclass
from typing import NamedTuple, List

import numpy as np


class City(NamedTuple):
    id: int
    x: int
    y: int
    demand: int


def distance(a: City, b: City):
    return abs(np.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2))


@dataclass
class Route:
    cities: List[List[City]]
    chromosome: List[City]
    score: float = None

    @property
    def fitness_score(self):
        if not self.score:
            self.score = 1 / np.sum([np.sum([distance(sub_route[i], sub_route[i + 1])
                                             for i in range(len(sub_route) - 1)])
                                     for sub_route in self.cities])
        return self.score

    @property
    def distance(self):
        return np.round(1 / self.fitness_score, 2)


class ProblemData(NamedTuple):
    name: str
    cities: List[City]
    depot: City
    truck_capacity: int
