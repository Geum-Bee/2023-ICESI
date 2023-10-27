# 2023 3 7 금비가 수정함


def run(graph, loc_dict, degree_num, t0, v, region, activate, city):
    if activate == 1:
        return cal.shortest_path_times(graph, loc_dict, degree_num, t0, v, region, activate, city)
    elif activate == 2:
        return cal.quickest_path_times(graph, loc_dict, degree_num, t0, v, region, activate, city)
    elif activate == 3:
        return cal.turn_shortest_path(graph, t0, 0, region, activate, city)
    elif activate == 4:
        return cal.shortest_path_dists(graph, loc_dict, t0, v, region, activate, city)


def main():
    select1 = int(input("short(1), mid(2), long(3) ? : "))
    select2 = int(input("속도를 설정하세요. (km/h) : "))
    select3 = int(input("shortest-path time(1) or quickest-path time(2) or turn-shortest-path(3) or shortest-path dist(4)?"))


    with open("txts/regions.txt", "r", encoding="UTF-8") as file:
        data = file.readlines()



    for i in range(len(data)):
        line                        = data[i].strip().split(",")
        # ans                       = int(line[0])
        city                        = line[1]
        region                      = line[2]
        t0                          = int(line[3]) + select1
        v                           = int(line[4]) + select2
        activate                    = int(line[5]) + select3

        print(city, region)

        loc_dict, degree_num, graph, tot_edge = setup.set_data(city, region)

        # print(graph)

        result                                = run(graph, loc_dict, degree_num, t0, v, region, activate, city)

        # print(result)



if __name__ == '__main__':
    import setup
    import cal

    main()