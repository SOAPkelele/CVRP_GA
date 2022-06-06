from typing import List

import matplotlib.pyplot as plt

from p_types import Route, ProblemData


def plot_solution(solution: Route, data: ProblemData):
    plt.title(f"Solution of {data.name}, distance: {solution.distance}")

    plt.scatter([city.x for city in data.cities], [city.y for city in data.cities],
                color='black', label='cities')

    colors = ['brown', 'pink', 'gray', 'cyan', 'red', 'green', 'blue', 'yellow', 'orange', 'purple',
              'brown', 'pink', 'gray', 'cyan', 'red', 'green', 'blue', 'yellow', 'orange', 'purple']

    for route in solution.cities:
        color = colors.pop()

        for i in range(len(route)):
            if i == len(route) - 1:
                plt.plot([route[i].x, route[0].x], [route[i].y, route[0].y], color=color, label=f'route {route[i].id}')
            else:
                plt.plot([route[i].x, route[i + 1].x], [route[i].y, route[i + 1].y],
                         color=color,
                         label=f"route #{i + 1}")
    plt.savefig(f"graphics/{data.name}_solution.png")
    plt.clf()


def plot_best_distances(distances: List[float], data: ProblemData):
    plt.title(f"Best distances of {data.name}")
    plt.plot(distances)
    plt.savefig(f"graphics/{data.name}_solution_distances.png")
    plt.clf()
