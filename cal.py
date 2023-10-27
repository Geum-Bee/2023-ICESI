from algorithms import *
import save
import numpy as np


def drone_dists(graph, loc_dict, t0, v, region, activate, city):
    drone_dist = get_drone_dist(graph, loc_dict, t0)

    if activate == 4 :
        save.save_data(t0, drone_dist, region, 0, v, city)

    return drone_dist


def shortest_path_dists(graph, loc_dict, t0, v, region, activate, city):
    drone_dist = drone_dists(graph, loc_dict, t0, v, region, activate, city)

    n = max(graph.keys())
    dist = np.zeros((n + 1, n + 1))

    for start in graph.keys():
        distances, parent = dijkstra(graph, start)
        for end in graph.keys():
            dist[start][end] = distances[end]

    dist[np.isinf(dist)] = 0                            # 프로그램 안정성 떄문에 넣음
    dist                 = dist.astype(int)
    dist                 = make_zero(drone_dist, dist)

    save.save_data(t0, dist, region, activate, v, city)

    return dist


def shortest_path_times(graph, loc_dict, degree_num, t0, v, region, activate, city):
    v = v * 1000 / 60  # m / min

    drone_dist    = drone_dists(graph, loc_dict, t0, v, region, activate, city)

    n             = max(graph.keys())
    original_time = np.zeros((n + 1, n + 1))
    edge_num      = np.zeros((n + 1, n + 1))
    plus_time     = np.zeros((n + 1, n + 1))

    for start in graph.keys():
        distances, parent = dijkstra(graph, start)
        for end in graph.keys():
            path = get_shortest_path(parent, end)
            plus = add(path, degree_num)
            edge_num[start][end]      = len(path) - 1
            original_time[start][end] = distances[end]
            plus_time[start][end]     = plus

    original_time = original_time / v * 60  # 단위 초
    original_time += plus_time

    make_zero(drone_dist, original_time)

    original_time[np.isinf(original_time)] = 0
    original_time /= 60
    original_time = np.around(original_time, 2)

    save.save_data(t0, original_time, region, activate, int(v / 1000 * 60), city)

    return original_time


def quickest_path_times(graph, loc_dict, degree_num, t0, v, region, activate, city):
    v = v * 1000 / 60  # m / min

    drone_dist    = drone_dists(graph, loc_dict, t0, v, region, activate, city)
    vertices_time = make_vertices_time(graph, degree_num)

    n = max(graph.keys())

    time        = np.empty((n + 1, n + 1))
    edge_num    = np.empty((n + 1, n + 1))
    time[:]     = np.nan
    edge_num[:] = np.nan

    for outer_key in graph:                             # graph 거리 -> 시간(초)로 환산
        for inner_key in graph[outer_key]:
            graph[outer_key][inner_key] = (graph[outer_key][inner_key] / v) * 60

    for start in graph.keys():
        distances, parent = find_quickest_path(graph, start, vertices_time)
        for end in graph.keys():
            path = get_quickest_path(parent, end)
            edge_num[start][end] = len(path) - 1
            time[start][end] = distances[end]

    make_nan(drone_dist, time)
    time /= 60
    time = np.around(time, 2)

    save.save_data(t0, time, region, activate, int(v / 1000 * 60), city)

    return time


def turn_shortest_path(graph, t0, v, region, activate, city) :
    # dists_list = []                                          # 튜플 왼쪽이 원래 edge 길이, 오른쪽이 돌아가는 shortest path 길이
    dists_ratio_list = []
    MAX_NUM = 9999999

    winding_road_cnt = 0

    for start in graph.keys() :
        for end in graph[start].keys() :
            original_edge_length      = graph[start][end]
            graph[start][end]         = MAX_NUM
            distances, parent         = dijkstra(graph, start)
            turn_shortest_path_dist   = distances[end]         #  돌아가는 shortest path는 하나밖에 없다.
            # dists_list.append((original_edge_length, turn_shortest_path_dist))
            if turn_shortest_path_dist == MAX_NUM :
                pass
            else :
                ratio                 = turn_shortest_path_dist / original_edge_length
                if ratio < 1 :                                 # 비율이 1 미만인 것들은 리스트에 포함 안함
                    winding_road_cnt += 1
                else :
                    ratio             = round(ratio, 2)
                    dists_ratio_list.append(ratio)
            graph[start][end]         = original_edge_length

    dists_ratio_list = np.array(dists_ratio_list)
    # print(" direct로 가는 거리가 sp보다 큰 edge의 개수 :", winding_road_cnt)

    save.save_data(t0, dists_ratio_list, region, activate, v, city)

    return winding_road_cnt                            # 튜플 두 번쨰 원소가 9999999는 돌아가는 길이 없다는 것임. (그 길이 유일하다.)


def resonable_paths():
    pass