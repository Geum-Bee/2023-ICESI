import heapq
from haversine import haversine
import numpy as np


def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    parent = {node: None for node in graph}
    queue = [(0, start)]

    while queue:
        (distance, current) = heapq.heappop(queue)
        if distance > distances[current]:
            continue
        for neighbor, cost in graph[current].items():
            new_distance = distance + cost
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                parent[neighbor] = current
                heapq.heappush(queue, (new_distance, neighbor))

    return distances, parent


def get_shortest_path(parent, end):
    path = [end]
    node = end
    while node is not None:
        node = parent[node]
        if node is not None:
            path.append(node)
    return path[::-1]


def get_drone_dist(graph, loc_dict, t0):
    num = max(graph.keys())

    hsin_m = np.zeros((num + 1, num + 1))

    for start in loc_dict.keys():
        for end in loc_dict.keys():
            hsin_m[start][end] = haversine(loc_dict[start], loc_dict[end], unit='m')  # 단위 m

    if t0 == 1 :
        hsin_m[(hsin_m >= 500)] = 0
    elif t0 == 2 :
        hsin_m[(hsin_m < 500) | (hsin_m >= 1500)] = 0
    elif t0 == 3 :
        hsin_m[(hsin_m < 1500)] = 0

    hsin_m = hsin_m.astype(int)

    return hsin_m


def add(path, degree_num):
    k = 30                               # degree에 대한 할당 값 단위 초
    C = 20                               # 단위 초
    init = 0
    for i in path:                       # 마지막 vertex는 도착하는 곳 이니깐 교차로 걸리는 시간 안구함
        if degree_num[i] - 2 <= 0:       # 시간 = C + k(d-2)
            init += C
        else:
            init += (C + (degree_num[i] - 2) * k)

    return init


def make_zero(arr1, arr2):
    zeros = np.where(arr1 == 0)
    arr2[zeros] = 0

    return arr2


def make_nan(arr1, arr2):
    zeros = np.where(arr1 == 0)
    arr2[zeros] = np.nan

    return arr2


def find_quickest_path(graph, start, vertices_time):
    distances = {vertex: float('inf') for vertex in graph}
    previous_vertices = {vertex: None for vertex in graph}
    distances[start] = 0
    vertices = [(0, start)]
    while vertices:
        (current_distance, current_vertex) = heapq.heappop(vertices)
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight + vertices_time[neighbor]
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_vertices[neighbor] = current_vertex
                heapq.heappush(vertices, (distance, neighbor))
    return distances, previous_vertices


def get_quickest_path(previous_vertices, end):
    path = []
    current_vertex = end
    while current_vertex is not None:
        path.append(current_vertex)
        next_vertex = previous_vertices[current_vertex]
        current_vertex = next_vertex
    path = path[::-1]

    return path


def make_vertices_time(graph, degree_num):
    vertices_time = {}

    k = 30  # degree에 대한 할당 값 단위 초
    C = 20  # 단위 초

    for i in graph.keys():
        if degree_num[i] - 2 <= 0:
            vertices_time[i] = C
        else:
            vertices_time[i] = (C + (degree_num[i] - 2) * k)

    return vertices_time