import pickle


def save_data(t0, data, region, activate, v, city) :
    if activate == 0:
        with open("data/" + city + "_" + region + "_" + str(t0) + "_" + str(v) + "_drone_dist.pkl", "wb") as f:
            pickle.dump(data, f)
    elif activate == 1:
        with open("data/" + city + "_" + region + "_" + str(t0) + "_" + str(v) + "_shortest_path_time.pkl", "wb") as f:
            pickle.dump(data, f)
    elif activate == 2:
        with open("data/" + city + "_" + region + "_" + str(t0) + "_" + str(v) + "_quickest_path_time.pkl", "wb") as f:
            pickle.dump(data, f)
    elif activate == 3:
        with open("data/" + city + "_" + region + "_" + str(0) + "_turn_shortest_path_ratios.pkl", "wb") as f:
            pickle.dump(data, f)
    elif activate == 4:
        with open("data/" + city + "_" + region + "_" + str(t0) + "_" + str(v) + "_shortest_path_dist.pkl", "wb") as f:
            pickle.dump(data, f)