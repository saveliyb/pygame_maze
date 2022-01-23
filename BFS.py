# import pygame as pg
from map import matrix_map
from settings import *
from collections import deque

# _ = False
# matrix_map = [
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, _, _, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, 1, _, _, _, _, _, 1],
#     [1, _, 1, 4, _, _, _, _, _, 1, 1, 1, _, _, _, 1, _, _, _, _, 1, _, _, 1],
#     [1, _, _, _, _, _, _, _, _, _, _, 1, 1, _, _, _, 1, _, _, _, _, _, _, 1],
#     [1, _, 1, 1, _, _, _, _, _, _, _, _, 1, _, 1, _, _, 1, _, _, _, 1, _, 1],
#     [1, _, _, _, _, _, 1, _, _, 1, 1, _, 1, _, _, _, _, _, _, 1, _, _, _, 1],
#     [1, _, 1, _, _, _, 1, _, _, 1, _, _, 1, _, _, _, 1, _, _, _, _, 1, _, 1],
#     [1, _, _, 1, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#     [1, _, 1, _, _, _, _, _, _, _, 1, _, _, 1, 1, _, _, _, _, 1, 1, _, _, 1],
#     [1, _, 1, _, _, _, 1, 1, _, 1, _, _, _, 1, 1, _, _, _, _, 1, 1, _, _, 1],
#     [1, _, _, _, _, 1, _, 1, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#     [1, _, 1, _, 1, _, _, _, _, 1, _, _, 1, _, _, _, _, _,  _, _, _, 1, _, 1],
#     [1, _, _, _, _, _, 1, _, _, _, _, _, 1, 1, _, _, _, _, _, _, 1, 1, _, 1],
#     [1, _, _, 1, _, _, _, _, 1, _, _, _, _, 1, 1, 1, 1, 1, 1, 1, 1, _, _, 5],
#     [1, _, _, _, _, _, _, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# ]


def get_rect(x, y):
    return x * TILE + 1, y * TILE + 1, TILE - 2, TILE - 2


def get_next_nodes(x, y):
    check_next_node = lambda x, y: True if 0 <= x < cols and 0 <= y < rows and not matrix_map[y][x] else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1]
    return [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]



def bfs(start, goal, graph):
    queue = deque([start])
    visited = {start: None}

    while queue:
        cur_node = queue.popleft()
        if cur_node == goal:
            break

        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            if next_node not in visited:
                queue.append(next_node)
                visited[next_node] = cur_node
    return queue, visited

cols, rows = len(matrix_map[0]), len(matrix_map)
TILE = 50

def map(matrix_map, start=(0, 0), finish=(0, 0)):
    graph = {}
    for y, row in enumerate(matrix_map):
        for x, col in enumerate(row):
            if finish == (0, 0):
                if col == 5:
                    if x == 0:
                        finish = (x + 1, y)
                    elif x == 23:
                        finish = (x - 1, y)
                    elif y == 0:
                        finish = (x, y + 1)
                    elif y == 17:
                        finish = (x, y - 1)
            if start == (0, 0):
                if col == 4:
                    start = (x, y - 1)
            elif not col:
                graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y)
    return (graph, start, finish)

def return_way(matrix_map, start=(0, 0), finish=(0, 0)):
    graph, start, finish = map(matrix_map, tuple(start), tuple(finish))
    print(start, finish)
    # queue = deque([start])
    visited = {start: None}
    # print(graph)
    queue, visited = bfs(start, finish, graph)
    # print(queue, visited)
    path_head, path_segment = finish, finish
    lst = []
    while path_segment and path_segment in visited:
        path_segment = visited[path_segment]
        lst.append(path_segment)
        # print(path_segment)
    lst = lst[:-1][::-1]
    print(lst)
    # graph.clear()
    return lst


# return_way()