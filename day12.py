from aocd import submit, lines
from graph import Graph
from collections import Counter
from helper_functions import time_function


def create_graph(input_edges):
    cave = Graph()
    for vertex in {vertex for line in input_edges for vertex in line.split('-')}:
        cave.add_vertex(vertex)

    # collect vertices in dictionary for easy access to the vertex objects
    vertices = {k.entity(): k for k in cave.vertices()}
    for edge in input_edges:
        origin, destination = edge.split('-')
        cave.add_edge(vertices[origin], vertices[destination])
    return cave, vertices


def small_cave_visited_twice(cur_path):
    counts = Counter(cur_path)
    for vertex in counts.keys():
        if vertex.islower() and counts[vertex] >= 2:
            return True
    return False


def get_all_paths(graph, paths, cur_path, cur_vertex, end, part='a'):
    for edge in graph.adjacent_edges(cur_vertex):
        next_vertex = edge.opposite(cur_vertex)
        next_vertex_name = next_vertex.entity()
        # print(f'\nCurrent vertex: {cur_vertex.entity()}')
        # print(f'Current path  : {cur_path}')
        # print(f'Next adjacent vertex: {next_vertex_name}')
        # print(f'Visited a small node twice already?: {small_cave_visited_twice(cur_path)}')
        if next_vertex_name == 'end':
            final_path = cur_path + [next_vertex_name]
            paths += [final_path]
            # print(f'Reached end node. The path to reach the end: {final_path}')
            # print(f'Current list of paths: {paths}')
        elif next_vertex_name.isupper() or next_vertex_name not in cur_path:
            new_path = cur_path[:] + [next_vertex_name]
            paths = get_all_paths(graph, paths, new_path, next_vertex, end, part)
        elif part == 'b' and next_vertex_name != 'start' and next_vertex_name in cur_path \
                and not small_cave_visited_twice(cur_path):
            new_path = cur_path[:] + [next_vertex_name]
            paths = get_all_paths(graph, paths, new_path, next_vertex, end, part)
    return paths


def run_part(part, input_edges, should_submit=False, print_output=False):
    cave, vertices = create_graph(input_edges)
    all_paths = get_all_paths(cave, [], ['start'], vertices['start'], vertices['end'], part)
    if print_output:
        for path in all_paths:
            print(path)
    answer = len(all_paths)
    print(f'The number of possible paths from "start" to "end" for part {part} is: {answer}')
    if should_submit:
        submit(answer, part=part)


with open('test12_2.txt', 'r') as f:
    #     start
    #     /   \
    # c--A-----b--d
    #     \   /
    #      end
    simple_example = f.read().splitlines()

with open('test12.txt', 'r') as f:
    medium_example = f.read().splitlines()

run_part('a', medium_example, False, True)
run_part('b', simple_example, False, True)
run_part('a', lines, True)
run_part('b', lines, True)
time_function(run_part, ['b', lines])
