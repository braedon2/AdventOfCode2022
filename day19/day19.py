import operator
import re
from functools import reduce

from numpy import array


def parse_blueprint(blueprint_str):
    a, b, c, d, e, f, g = [int(n) for n in re.findall(r'\d+', blueprint_str)]
    return a, {
        (0, 0, 0, 1): array((0, 0, 0, b)),
        (0, 0, 1, 0): array((0, 0, 0, c)),
        (0, 1, 0, 0): array((0, 0, e, d)),
        (1, 0, 0, 0): array((0, g, 0, f)),
        (0, 0, 0, 0): array((0, 0, 0, 0))
    }

def foo(x):
    a1, a2, a3, a4 = x[0]
    b1, b2, b3, b4 = x[1]
    return (b1, a1, b2, a2, b3, a3, b4, a4)


def prune(generation_to_prune):
    return sorted(generation_to_prune, key=foo, reverse=True)[:20000]



def run_blueprint(identifier, blueprint, time):
    generation = [(array((0, 0, 0, 1)), array((0, 0, 0, 0)))]  # root generation of decision tree

    for _ in range(time):
        next_generation = []
        for production_capacity, resources in generation:
            for robot, cost in blueprint.items():
                if all(cost <= resources):
                    next_generation.append((
                        production_capacity + array(robot),
                        resources - cost + production_capacity
                    ))
        generation = prune(next_generation)

    return max(x[1][0] for x in generation) #* identifier


with open('puzzle_input') as file:
    # part A
    blueprints = [parse_blueprint(line) for line in file.readlines()][:3]
    # print(sum([run_blueprint(i, bp, 24) for i, bp in blueprints]))

    # part B
    #blueprints = blueprints[:2]
    #print([run_blueprint(i, bp, 32) for i, bp in blueprints])
    print(reduce(operator.mul, [run_blueprint(i, bp, 32) for i, bp in blueprints]))
