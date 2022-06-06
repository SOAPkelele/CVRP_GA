from p_types import City, ProblemData


def parse_data(file: str):
    nodes = 0
    capacity = 0
    nodes_cords = {}
    demand_d = {}

    with open(file, "r") as f:
        lines = f.readlines()

        for i, line in enumerate(lines):
            if line.startswith("DIMENSION"):
                nodes = int(line.split()[-1])

            if line.startswith("CAPACITY"):
                capacity = int(line.split()[-1])

            if line.startswith("NODE_COORD_SECTION"):
                for coord_line in lines[i + 1:]:
                    if coord_line.startswith("DEMAND_SECTION"):
                        break
                    node, coord_x, coord_y = map(float, coord_line.split())
                    nodes_cords[node - 1] = (coord_x, coord_y)

            if line.startswith("DEMAND_SECTION"):
                for demand_line in lines[i + 1:]:
                    if demand_line.startswith("DEPOT_SECTION"):
                        break
                    node, demand = map(int, demand_line.split())
                    demand_d[node - 1] = demand

    return ProblemData(name=file.split(".")[0].split("/")[-1],
                       truck_capacity=capacity,
                       cities=[City(i, nodes_cords[i][0], nodes_cords[i][1], demand_d[i]) for i in
                               range(1, nodes)],
                       depot=City(0, nodes_cords[0][0], nodes_cords[0][1], 0))


def parse_solution(file: str):
    with open(file, "r") as f:
        lines = f.readlines()

        routes = {}
        for i, line in enumerate(lines):
            if line.startswith("Route"):
                nodes = line.split(": ")[-1].split(" ")

                try:
                    nodes.remove("\n")
                except:
                    pass

                route = list(map(int, nodes))
                routes[i] = route

            if line.startswith("Cost"):
                cost = float(line.split()[-1])
    return cost, routes
